"use client";
import React, { useState } from "react";
import Image from "next/image";
import { Send, Paperclip, Smile } from "lucide-react";

export default function ChatPage() {
  const [messages, setMessages] = useState([
    {
      sender: "MineMate",
      text: "Hi there! I'm MineMate, your mental health companion. How are you feeling today?",
      type: "bot",
    },
    {
      sender: "Alex",
      text: "I’m feeling a bit stressed with work deadlines.",
      type: "user",
    },
    {
      sender: "MineMate",
      text: "I understand. Work stress can be tough. Let’s explore some strategies to manage it. Have you tried any relaxation techniques before?",
      type: "bot",
    },
  ]);

  const [input, setInput] = useState("");

  const sendMessage = (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    setMessages([...messages, { sender: "Alex", text: input, type: "user" }]);
    setInput("");
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* NAVBAR */}
      <nav className="w-full bg-white shadow-sm">
        <div className="max-w-7xl mx-auto flex items-center justify-between px-6 py-4">
          {/* Left Logo */}
          <div className="flex items-center space-x-2">
            <span className="w-3 h-3 bg-black rounded-full"></span>
            <span className="font-bold text-lg">MineMate</span>
          </div>

          {/* Right Menu */}
          <div className="flex items-center space-x-6">
            <a href="/" className="text-gray-700 hover:text-blue-500">
              Home
            </a>
            <a href="/about" className="text-gray-700 hover:text-blue-500">
              About
            </a>
            <a href="/profile" className="text-gray-700 hover:text-blue-500">
              Profile
            </a>
            <button className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600">
              Logout
            </button>
            <Image
              src="/user.png" // replace with actual profile image
              alt="profile"
              width={32}
              height={32}
              className="rounded-full"
            />
          </div>
        </div>
      </nav>

      {/* MAIN CONTENT */}
      <main className="flex flex-1 max-w-7xl mx-auto w-full px-6 py-6 gap-8">
        {/* CHAT SECTION */}
        <div className="flex-1 bg-white rounded-xl shadow flex flex-col">
          <h2 className="text-xl font-bold p-4 border-b">
            Chat with MineMate - Your Mental Health Companion
          </h2>

          {/* Messages */}
          <div className="flex-1 p-4 space-y-4 overflow-y-auto">
            {messages.map((msg, i) => (
              <div
                key={i}
                className={`flex items-end ${
                  msg.type === "user" ? "justify-end" : "justify-start"
                }`}
              >
                {/* Bot avatar */}
                {msg.type === "bot" && (
                  <Image
                    src="/bot.png" // replace with bot avatar image
                    alt="MineMate"
                    width={36}
                    height={36}
                    className="rounded-full mr-2"
                  />
                )}

                {/* Message bubble */}
                <div
                  className={`p-3 rounded-lg max-w-md ${
                    msg.type === "user"
                      ? "bg-blue-500 text-white rounded-br-none"
                      : "bg-gray-100 text-gray-800 rounded-bl-none"
                  }`}
                >
                  <p className="text-sm">{msg.text}</p>
                  <span className="block text-xs mt-1 opacity-70">
                    {msg.sender}
                  </span>
                </div>

                {/* User avatar */}
                {msg.type === "user" && (
                  <Image
                    src="/user.png" // replace with Alex’s avatar
                    alt="Alex"
                    width={36}
                    height={36}
                    className="rounded-full ml-2"
                  />
                )}
              </div>
            ))}
          </div>

          {/* Input Box */}
          <form
            onSubmit={sendMessage}
            className="flex items-center p-4 border-t space-x-3"
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
              className="flex-1 border border-gray-300 rounded-lg p-2"
            />
            <Paperclip className="text-gray-500 cursor-pointer" />
            <Smile className="text-gray-500 cursor-pointer" />
            <button
              type="submit"
              className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 flex items-center gap-1"
            >
              <Send size={16} /> Send
            </button>
          </form>
        </div>

        {/* SIDEBAR */}
        <aside className="w-72 bg-white rounded-xl shadow p-6 flex flex-col items-center">
          <Image
            src="/user.png" // replace with actual profile pic
            alt="Alex"
            width={100}
            height={100}
            className="rounded-full mb-4"
          />
          <h3 className="text-lg font-semibold">Alex</h3>
          <p className="text-gray-500 text-sm">Mood: Neutral</p>

          {/* Tips */}
          <div className="mt-6 text-sm text-gray-700 space-y-2">
            <h4 className="font-medium">Personalized Wellness Tips</h4>
            <p>
              Consider taking short breaks, practicing mindfulness, or setting
              clear boundaries between work and personal life.
            </p>
          </div>

          {/* Button */}
          <div className="mt-6 w-full">
            <button className="w-full bg-gray-100 hover:bg-gray-200 rounded-lg py-2 font-medium">
              Find a Therapist
            </button>
          </div>
        </aside>
      </main>
    </div>
  );
}
