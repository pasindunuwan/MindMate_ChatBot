from typing import Any, Text, Dict, List, Tuple
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
import logging
import openai
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from twilio.rest import Client
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Load .env file
load_dotenv(dotenv_path=r"E:\MainProjectFile\MindMate ChatBot\MindMate_BackEnd\.env")

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Set OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')
if not openai.api_key:
    logger.error("OPENAI_API_KEY not found in .env file")
    raise ValueError("OPENAI_API_KEY not found in .env file")

# Twilio configuration
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
RESPONSIBLE_PERSON_PHONE = os.getenv('RESPONSIBLE_PERSON_PHONE')

# Spotify configuration
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
if not all([SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET]):
    logger.error("Spotify credentials not found in .env file")
    raise ValueError("Spotify credentials not found in .env file")

# Initialize Spotify client
try:
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET
    ))
except Exception as e:
    logger.error(f"Spotify initialization error: {e}")
    raise ValueError(f"Failed to initialize Spotify client: {e}")

# Full DASS-21 Questions
DASS_21_QUESTIONS = [
    {"text": "I found it hard to wind down?", "scale": "stress"},
    {"text": "I was aware of dryness of my mouth?", "scale": "anxiety"},
    {"text": "I couldn’t seem to experience any positive feeling at all?", "scale": "depression"},
    {"text": "I experienced breathing difficulty (e.g., excessively rapid breathing, breathlessness in the absence of physical exertion)?", "scale": "anxiety"},
    {"text": "I found it difficult to work up the initiative to do things?", "scale": "depression"},
    {"text": "I tended to over-react to situations?", "scale": "stress"},
    {"text": "I experienced trembling (e.g., in the hands)?", "scale": "anxiety"},
    {"text": "I felt that I was using a lot of nervous energy?", "scale": "stress"},
    {"text": "I was worried about situations in which I might panic and make a fool of myself?", "scale": "anxiety"},
    {"text": "I felt that I had nothing to look forward to?", "scale": "depression"},
    {"text": "I found myself getting agitated?", "scale": "stress"},
    {"text": "I found it difficult to relax?", "scale": "stress"},
    {"text": "I felt down-hearted and blue?", "scale": "depression"},
    {"text": "I was intolerant of anything that kept me from getting on with what I was doing?", "scale": "stress"},
    {"text": "I felt I was close to panic?", "scale": "anxiety"},
    {"text": "I was unable to become enthusiastic about anything?", "scale": "depression"},
    {"text": "I felt I wasn’t worth much as a person?", "scale": "depression"},
    {"text": "I felt that I was rather touchy?", "scale": "stress"},
    {"text": "I was aware of the action of my heart in the absence of physical exertion (e.g., sense of heart rate increase, heart missing a beat)?", "scale": "anxiety"},
    {"text": "I felt scared without any good reason?", "scale": "anxiety"},
    {"text": "I felt that life was meaningless?", "scale": "depression"},
]

# DASS-21 Scoring Levels
def get_dass_level(score: float, scale: Text) -> Text:
    if scale == "depression":
        if score <= 9:
            return "Normal"
        elif score <= 13:
            return "Mild"
        elif score <= 20:
            return "Moderate"
        elif score <= 27:
            return "Severe"
        else:
            return "Extremely Severe"
    elif scale == "anxiety":
        if score <= 7:
            return "Normal"
        elif score <= 9:
            return "Mild"
        elif score <= 14:
            return "Moderate"
        elif score <= 19:
            return "Severe"
        else:
            return "Extremely Severe"
    elif scale == "stress":
        if score <= 14:
            return "Normal"
        elif score <= 18:
            return "Mild"
        elif score <= 25:
            return "Moderate"
        elif score <= 33:
            return "Severe"
        else:
            return "Extremely Severe"
    return "Normal"

# Send SMS to responsible person
def send_sms_notification(scores: List[Tuple[Text, float, Text]], user_id: Text):
    if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, RESPONSIBLE_PERSON_PHONE]):
        logger.error("Twilio environment variables not set.")
        return

    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message_body = f"DASS-21 Results: "
        message_body += ", ".join([f"{scale} - {level} ({score})" for scale, score, level in scores])
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE_NUMBER,
            to=RESPONSIBLE_PERSON_PHONE
        )
        logger.info(f"SMS sent successfully: {message.sid}")
    except Exception as e:
        logger.error(f"Failed to send SMS: {e}")

# Spotify playlist recommendations based on DASS-21 levels
def get_spotify_playlist(scale: Text, level: Text) -> Dict[Text, Any]:
    try:
        # Define search queries based on scale and level
        if scale == "Depression":
            if level == "Mild":
                query = "uplifting acoustic playlist"
            elif level == "Moderate":
                query = "motivational pop playlist"
        elif scale == "Anxiety":
            if level == "Mild":
                query = "calm instrumental playlist"
            elif level == "Moderate":
                query = "relaxing lo-fi playlist"
        elif scale == "Stress":
            if level == "Mild":
                query = "peaceful ambient playlist"
            elif level == "Moderate":
                query = "chill meditation playlist"
        else:
            return {"name": None, "url": None}

        # Search Spotify for playlists
        results = sp.search(q=query, type="playlist", limit=1)
        playlists = results["playlists"]["items"]
        if playlists:
            playlist = playlists[0]
            return {
                "name": playlist["name"],
                "url": playlist["external_urls"]["spotify"]
            }
        else:
            logger.warning(f"No playlist found for query: {query}")
            return {"name": None, "url": None}
    except Exception as e:
        logger.error(f"Spotify API error for {scale} ({level}): {e}")
        return {"name": None, "url": None}

class ActionAskDassQuestion(Action):
    def name(self) -> Text:
        return "action_ask_dass_question"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        question_index = tracker.get_slot("question_index") or 0
        logger.debug(f"ActionAskDassQuestion: question_index={question_index}, type={type(question_index)}")
        try:
            question_index = float(question_index)
        except (TypeError, ValueError):
            logger.warning(f"Invalid question_index: {question_index}. Resetting to 0.")
            question_index = 0.0

        if question_index >= len(DASS_21_QUESTIONS):
            logger.debug("All questions answered. Triggering action_show_dass_results.")
            return [SlotSet("question_index", 0), FollowupAction("action_show_dass_results")]

        question = DASS_21_QUESTIONS[int(question_index)]["text"]
        dispatcher.utter_message(response="utter_ask_question", question=question)
        return [SlotSet("current_question", question), SlotSet("question_index", question_index + 1)]

class ActionProcessDassResponse(Action):
    def name(self) -> Text:
        return "action_process_dass_response"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_response = tracker.latest_message.get("text")
        logger.debug(f"ActionProcessDassResponse: user_response={user_response}")
        try:
            score = int(user_response)
            if score not in [0, 1, 2, 3]:
                logger.warning(f"Invalid score: {score}. Requesting valid response.")
                dispatcher.utter_message(response="utter_invalid_response")
                return [SlotSet("question_index", tracker.get_slot("question_index") - 1)]
        except ValueError:
            logger.warning(f"Non-numeric response: {user_response}. Requesting valid response.")
            dispatcher.utter_message(response="utter_invalid_response")
            return [SlotSet("question_index", tracker.get_slot("question_index") - 1)]

        question_index = tracker.get_slot("question_index") - 1
        logger.debug(f"Processing response for question_index={question_index}")
        try:
            question_index = float(question_index)
        except (TypeError, ValueError):
            logger.warning(f"Invalid question_index: {question_index}. Resetting to 0.")
            dispatcher.utter_message(response="utter_invalid_response")
            return [SlotSet("question_index", 0)]

        if question_index < 0 or question_index >= len(DASS_21_QUESTIONS):
            logger.warning(f"question_index out of bounds: {question_index}. Resetting to 0.")
            dispatcher.utter_message(response="utter_invalid_response")
            return [SlotSet("question_index", 0)]

        scale = DASS_21_QUESTIONS[int(question_index)]["scale"]
        depression_score = float(tracker.get_slot("depression_score") or 0)
        anxiety_score = float(tracker.get_slot("anxiety_score") or 0)
        stress_score = float(tracker.get_slot("stress_score") or 0)

        if scale == "depression":
            depression_score += score
        elif scale == "anxiety":
            anxiety_score += score
        elif scale == "stress":
            stress_score += score

        logger.debug(f"Updated scores: depression={depression_score}, anxiety={anxiety_score}, stress={stress_score}")
        events = [
            SlotSet("depression_score", depression_score),
            SlotSet("anxiety_score", anxiety_score),
            SlotSet("stress_score", stress_score),
        ]

        return events + [FollowupAction("action_ask_dass_question")]

class ActionShowDassResults(Action):
    def name(self) -> Text:
        return "action_show_dass_results"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        depression_score = float(tracker.get_slot("depression_score") or 0) * 2
        anxiety_score = float(tracker.get_slot("anxiety_score") or 0) * 2
        stress_score = float(tracker.get_slot("stress_score") or 0) * 2

        depression_level = get_dass_level(depression_score, "depression")
        anxiety_level = get_dass_level(anxiety_score, "anxiety")
        stress_level = get_dass_level(stress_score, "stress")

        logger.debug(f"Showing results: depression={depression_score} ({depression_level}), anxiety={anxiety_score} ({anxiety_level}), stress={stress_score} ({stress_level})")
        dispatcher.utter_message(
            response="utter_show_results",
            depression_score=depression_score,
            depression_level=depression_level,
            anxiety_score=anxiety_score,
            anxiety_level=anxiety_level,
            stress_score=stress_score,
            stress_level=stress_level
        )

        # Store scores in temporary slots before resetting
        events = [
            SlotSet("temp_depression_score", depression_score),
            SlotSet("temp_anxiety_score", anxiety_score),
            SlotSet("temp_stress_score", stress_score),
            SlotSet("depression_score", 0),
            SlotSet("anxiety_score", 0),
            SlotSet("stress_score", 0),
            SlotSet("question_index", 0),
            SlotSet("current_question", None),
            FollowupAction("action_retrieve_and_generate_tips")
        ]
        return events

class ActionRetrieveAndGenerateTips(Action):
    def name(self) -> Text:
        return "action_retrieve_and_generate_tips"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Use temporary slots to get correct scores
        depression_score = float(tracker.get_slot("temp_depression_score") or 0)
        anxiety_score = float(tracker.get_slot("temp_anxiety_score") or 0)
        stress_score = float(tracker.get_slot("temp_stress_score") or 0)
        logger.debug(f"Retrieved temp scores: depression={depression_score}, anxiety={anxiety_score}, stress={stress_score}")

        # Get levels for all scales
        scales = [
            ("Depression", depression_score, get_dass_level(depression_score, "depression")),
            ("Anxiety", anxiety_score, get_dass_level(anxiety_score, "anxiety")),
            ("Stress", stress_score, get_dass_level(stress_score, "stress"))
        ]
        logger.debug(f"Scales: {scales}")

        # Check for severe/extremely severe cases
        any_severe = any(level in ["Severe", "Extremely Severe"] for _, _, level in scales)
        if any_severe:
            user_id = tracker.sender_id or "Unknown"
            logger.debug(f"Sending SMS for user {user_id} with scores: {scales}")
            send_sms_notification(scales, user_id)
            dispatcher.utter_message(text="Your results indicate serious concerns. Please meet a doctor or mental health professional immediately, such as by calling the 988 Crisis Lifeline (US) or contacting an Employee Assistance Program (EAP).")

        # Initialize response and context
        response_text = "### Relaxation Tips for Remote Workers\nAs a remote worker, it’s essential to prioritize your mental well-being. Below are tailored messages for each of your DASS-21 results.\n"
        music_recommendations = []
        rag_context = ""

        # Load SentenceTransformer and FAISS index
        try:
            model = SentenceTransformer('all-MiniLM-L6-v2')
            index = faiss.read_index(r"E:\MainProjectFile\MindMate ChatBot\MindMate_BackEnd\pdf_knowledge_base_index.faiss")
            with open(r"E:\MainProjectFile\MindMate ChatBot\MindMate_BackEnd\text_metadata.txt", 'r') as f:
                doc_paths = f.read().splitlines()
            logger.debug(f"Loaded FAISS index and {len(doc_paths)} metadata entries")
        except Exception as e:
            logger.error(f"RAG setup error: {e}")
            response_text += (
                "I’m sorry, I couldn’t retrieve specific tips due to an error. "
                "For serious concerns, please contact a professional, such as a therapist or the 988 Crisis Lifeline (US). "
                "Here’s a general suggestion: Inhale deeply for 4 seconds, hold for 4, exhale for 4. Repeat 5 times.\n"
                "I am not a therapist; please consult a professional for serious concerns."
            )
            logger.debug(f"Response text before dispatch: {response_text}")
            dispatcher.utter_message(text=response_text)
            return [SlotSet("rag_context", "Default relaxation tip: Try deep breathing exercises."), SlotSet("music_recommendations", None)]

        # Process each scale
        for scale_name, score, level in scales:
            logger.debug(f"Processing scale: {scale_name}, score={score}, level={level}")
            if level == "Normal":
                logger.debug(f"Skipping tips for {scale_name} due to Normal level")
                response_text += (
                    f"\n#### {scale_name} ({level}, Score: {score})\n"
                    f"Your {scale_name.lower()} level is Normal, indicating good mental health in this area. Keep up your positive habits!\n"
                )
                continue
            elif level in ["Severe", "Extremely Severe"]:
                logger.debug(f"Skipping music recommendations for {scale_name} due to {level} level")
                response_text += (
                    f"\n#### {scale_name} ({level}, Score: {score})\n"
                    f"Your {scale_name.lower()} score indicates serious concerns. Please meet a doctor or mental health professional immediately, such as by calling the 988 Crisis Lifeline (US) or an Employee Assistance Program (EAP). "
                    f"For now, try this basic technique: Inhale deeply for 4 seconds, hold for 4, exhale for 4. Repeat 5 times.\n"
                )
                continue

            # Get Spotify playlist for Mild/Moderate levels
            playlist = get_spotify_playlist(scale_name, level)
            if playlist["name"] and playlist["url"]:
                music_recommendations.append(f"{scale_name} ({level}): Try listening to '{playlist['name']}' on Spotify: {playlist['url']}")
            else:
                music_recommendations.append(f"{scale_name} ({level}): Couldn’t find a specific playlist. Try searching for calming music on Spotify.")

            # Form RAG query for non-Normal levels
            query = f"relaxation tips for {level.lower()} {scale_name.lower()} in remote workers"
            logger.debug(f"RAG query for {scale_name}: {query}")

            # Retrieve relevant chunks
            try:
                query_embedding = model.encode([query])
                D, I = index.search(np.array(query_embedding), k=2)
                context = "\n".join([open(f"E:\\MainProjectFile\\MindMate ChatBot\\MindMate_BackEnd\\text_knowledge_base\\{doc_paths[i]}", 'r', encoding='utf-8').read() for i in I[0] if i >= 0])
                rag_context += f"{scale_name}: {context}\n"
                logger.debug(f"Retrieved context for {scale_name}: {context[:100]}...")
            except Exception as e:
                logger.error(f"RAG retrieval error for {scale_name}: {e}")
                context = f"Default relaxation tip for {scale_name}: Try deep breathing exercises."
                response_text += (
                    f"\n#### {scale_name} ({level}, Score: {score})\n"
                    f"I couldn’t retrieve specific tips for {scale_name.lower()}. Here’s a general suggestion: Inhale deeply for 4 seconds, hold for 4, exhale for 4. Repeat 5 times.\n"
                )
                continue

            # Generate response with OpenAI for non-Normal levels
            prompt = (
                f"User: remote worker, {level} {scale_name} (score: {score}). "
                f"Context: {context}. "
                f"Give one concise relaxation technique with 2-3 steps. "
                f"For severe/extremely severe, stress professional help (e.g., 988/EAP) and use basic techniques."
            )
            logger.debug(f"Prompt for {scale_name}: {prompt[:100]}...")
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=200
                ).choices[0].message.content
                response_text += f"\n#### {scale_name} ({level}, Score: {score})\n{response}\n"
                logger.debug(f"Generated response for {scale_name}: {response}")
            except Exception as e:
                logger.error(f"OpenAI API error for {scale_name}: {e}")
                response_text += (
                    f"\n#### {scale_name} ({level}, Score: {score})\n"
                    f"I couldn’t generate specific tips for {scale_name.lower()}. Try: Inhale deeply for 4s, hold for 4s, exhale for 4s. Repeat 5 times.\n"
                )

        # Add music recommendations to response
        if music_recommendations:
            response_text += "\n### Music Recommendations\nListening to music can help improve your mood. Here are some Spotify playlists tailored to your results:\n"
            response_text += "\n".join(music_recommendations) + "\n"

        # Add disclaimer
        response_text += "\nI am not a therapist; please consult a professional for serious concerns."
        logger.debug(f"Final response text: {response_text}")

        # Dispatch response and clear temporary slots
        dispatcher.utter_message(text=response_text)
        return [
            SlotSet("rag_context", rag_context),
            SlotSet("music_recommendations", "\n".join(music_recommendations) if music_recommendations else None),
            SlotSet("temp_depression_score", None),
            SlotSet("temp_anxiety_score", None),
            SlotSet("temp_stress_score", None)
        ]

class ActionAnswerGeneralQuestion(Action):
    def name(self) -> Text:
        return "action_answer_general_question"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_question = tracker.latest_message.get("text")
        logger.debug(f"ActionAnswerGeneralQuestion: user_question={user_question}")

        # Check if question is related to mental health
        mental_health_keywords = ["depression", "anxiety", "stress", "mental health", "relaxation", "well-being", "therapy"]
        is_mental_health_related = any(keyword in user_question.lower() for keyword in mental_health_keywords)

        if is_mental_health_related:
            # Use RAG for mental health questions
            try:
                model = SentenceTransformer('all-MiniLM-L6-v2')
                index = faiss.read_index(r"E:\MainProjectFile\MindMate ChatBot\MindMate_BackEnd\pdf_knowledge_base_index.faiss")
                with open(r"E:\MainProjectFile\MindMate ChatBot\MindMate_BackEnd\text_metadata.txt", 'r') as f:
                    doc_paths = f.read().splitlines()
                logger.debug(f"Loaded FAISS index and {len(doc_paths)} metadata entries for general question")

                # Retrieve relevant chunks
                query_embedding = model.encode([user_question])
                D, I = index.search(np.array(query_embedding), k=2)
                context = "\n".join([open(f"E:\\MainProjectFile\\MindMate ChatBot\\MindMate_BackEnd\\text_knowledge_base\\{doc_paths[i]}", 'r', encoding='utf-8').read() for i in I[0] if i >= 0])
                logger.debug(f"Retrieved context for question: {context[:100]}...")

                # Generate response with OpenAI
                prompt = (
                    f"User question: {user_question}. "
                    f"Context: {context}. "
                    f"Provide a concise, helpful answer for a remote worker. If the question is about mental health, offer practical advice or resources. "
                    f"For serious concerns, suggest consulting a professional (e.g., 988 Crisis Lifeline or EAP)."
                )
                response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=200
                ).choices[0].message.content
                logger.debug(f"Generated response: {response}")
            except Exception as e:
                logger.error(f"Error processing mental health question: {e}")
                response = (
                    "I’m sorry, I couldn’t retrieve specific information. For mental health concerns, try deep breathing: "
                    "Inhale for 4 seconds, hold for 4, exhale for 4. Repeat 5 times. "
                    "For serious issues, contact a professional, such as the 988 Crisis Lifeline (US) or an EAP."
                )
        else:
            # Direct OpenAI query for non-mental health questions
            try:
                prompt = (
                    f"User question: {user_question}. "
                    f"Provide a concise, helpful answer for a remote worker."
                )
                response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=200
                ).choices[0].message.content
                logger.debug(f"Generated response: {response}")
            except Exception as e:
                logger.error(f"OpenAI API error: {e}")
                response = "I’m sorry, I couldn’t process your question. Please try again or ask something else."

        dispatcher.utter_message(response="utter_general_answer", answer=response)
        return []