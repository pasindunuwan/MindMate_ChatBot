import React from "react";
import Image from "next/image";
import loginImg from "/public/login.png"; // replace with your actual image path

export default function Login() {
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
              Log Out
            </button>
          </div>
        </div>
      </nav>

      {/* MAIN CONTENT */}
      <main className="flex-1 flex flex-col items-center justify-center px-6 py-12">
        {/* Heading */}
        <div className="text-center mb-10">
          <h1 className="text-3xl font-bold text-gray-900">
            Welcome Back to MineMate
          </h1>
          <p className="mt-2 text-gray-600 max-w-lg">
            Your journey to a healthier mind continues. Log in to access your
            personalized support and resources.
          </p>
        </div>

        {/* Content Box */}
        <div className="flex flex-col md:flex-row items-center justify-center bg-white rounded-xl shadow p-8 md:p-12 max-w-5xl w-full gap-x-12">
          {/* Left Image */}
          <div className="w-full md:w-1/2 flex justify-center mb-6 md:mb-0">
            <Image
              src={loginImg}
              alt="Login illustration"
              className="rounded-lg w-80 md:w-full h-auto"
            />
          </div>

          {/* Right Form */}
          <div className="w-full md:w-1/2 flex justify-center">
            <div className="w-full max-w-sm">
              <form className="space-y-5">
                <div>
                  <label className="block text-sm font-medium">Email</label>
                  <input
                    type="email"
                    placeholder="Enter your email"
                    className="w-full border border-gray-300 rounded-lg p-2 mt-1"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium">Password</label>
                  <input
                    type="password"
                    placeholder="Enter your password"
                    className="w-full border border-gray-300 rounded-lg p-2 mt-1"
                  />
                </div>
                <button
                  type="submit"
                  className="w-full bg-blue-500 text-white rounded-lg py-2 hover:bg-blue-600"
                >
                  Log In
                </button>
              </form>

              {/* Extra Links */}
              <div className="flex flex-col items-center text-sm mt-4 space-y-2">
                <p>
                  Don’t have an account?{" "}
                  <a href="/signup" className="text-blue-500 hover:underline">
                    Sign up.
                  </a>
                </p>
                <a
                  href="/forgot-password"
                  className="text-gray-500 hover:underline"
                >
                  Forgot Password?
                </a>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
