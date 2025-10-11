import Image from "next/image";
import signupImg from "/public/sign_up.png"; // Add your image to public folder

export default function Signup() {
  return (
    <div className="min-h-screen bg-white font-sans">
      {/* Navbar */}
      <nav className="flex justify-between items-center p-6 shadow-md">
        <div className="text-xl font-bold flex items-center gap-2">
          <span className="w-3 h-3 bg-black rounded-sm"></span>
          MineMate
        </div>
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
            Log Out
          </button>
        </div>
      </nav>

      {/* Heading */}
      <div className="text-center mt-10 mb-8 px-4">
        <h1 className="text-3xl md:text-4xl font-extrabold leading-snug">
          Join MineMate and take the first step <br />
          towards better mental wellbeing.
        </h1>
      </div>

      {/* Main Box (Image + Form) */}
      <div className="max-w-5xl mx-auto border rounded-lg shadow-md p-8 grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
        {/* Left: Image */}
        <div className="flex justify-center">
          <Image
            src={signupImg}
            alt="Signup Illustration"
            width={400}
            height={400}
            className="rounded-lg object-contain"
          />
        </div>

        {/* Right: Form */}
        <div>
          <form className="space-y-5">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Full Name
              </label>
              <input
                type="text"
                placeholder="Enter your full name"
                className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Email
              </label>
              <input
                type="email"
                placeholder="Enter your email"
                className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Password
              </label>
              <input
                type="password"
                placeholder="Enter your password"
                className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Confirm Password
              </label>
              <input
                type="password"
                placeholder="Confirm your password"
                className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <button
              type="submit"
              className="w-full bg-blue-500 text-white py-3 rounded-lg hover:bg-blue-600 transition"
            >
              Create Account
            </button>
          </form>

          {/* Centered login text */}
          <div className="text-center mt-3">
            <p className="text-sm text-gray-600">
              Already have an account?{" "}
              <a href="#" className="text-blue-500 hover:underline">
                Log in
              </a>
              .
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
