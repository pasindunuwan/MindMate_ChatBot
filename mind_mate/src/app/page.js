import Image from "next/image";
import mineMateImg from "/public/homepage.png"; // Add your uploaded image to public folder

export default function Home() {
  return (
    <div className="min-h-screen bg-white font-sans">
      {/* Navigation */}
      <nav className="flex justify-between items-center p-6 shadow-md">
        <div className="text-xl font-bold">MineMate</div>
        <div className="space-x-4">
          <a href="#" className="text-gray-700 hover:text-gray-900">
            Home
          </a>
          <a href="#" className="text-gray-700 hover:text-gray-900">
            About
          </a>
          <a href="#" className="text-gray-700 hover:text-gray-900">
            Profile
          </a>
          <button className="bg-blue-500 text-white px-4 py-1 rounded-lg hover:bg-blue-600">
            Signup
          </button>
          <button className="bg-blue-500 text-white px-4 py-1 rounded-lg hover:bg-blue-600">
            Login
          </button>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="flex flex-col md:flex-row items-center justify-center w-full h-screen px-6">
        <div className="md:w-1/2 flex justify-center mb-10 md:mb-0">
          <Image
            src={mineMateImg}
            alt="MineMate"
            width={600} // ⬅️ Bigger width
            height={400} // ⬅️ Bigger height
            className="rounded-lg shadow-lg object-contain"
          />
        </div>
        <div className="md:w-1/2 md:pl-16 text-center md:text-left">
          <h1 className="text-5xl font-extrabold mb-6">
            Your Mental Wellness, Simplified
          </h1>
          <p className="text-gray-700 mb-8 text-lg">
            MineMate is your personal mental health companion, designed to
            support remote workers in managing stress, improving focus, and
            fostering a positive mindset.
          </p>
          <button className="bg-blue-500 text-white px-8 py-3 rounded-lg hover:bg-blue-600">
            Get Started
          </button>
        </div>
      </section>
    </div>
  );
}
