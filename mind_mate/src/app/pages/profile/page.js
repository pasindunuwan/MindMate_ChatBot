"use client";
import React from "react";
import Image from "next/image";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

export default function ProfilePage() {
  const data = [
    { day: "Mon", mood: 70 },
    { day: "Tue", mood: 65 },
    { day: "Wed", mood: 60 },
    { day: "Thu", mood: 68 },
    { day: "Fri", mood: 80 },
    { day: "Sat", mood: 90 },
    { day: "Sun", mood: 75 },
  ];

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
      <main className="flex-1 max-w-5xl mx-auto w-full px-6 py-8 space-y-10">
        {/* Profile Info */}
        <section>
          <h1 className="text-2xl font-bold mb-6">Your Profile - MineMate</h1>
          <div className="flex items-center space-x-6">
            <Image
              src="/user.png" // replace with actual profile image
              alt="profile"
              width={80}
              height={80}
              className="rounded-full"
            />
            <div>
              <h2 className="font-semibold text-lg">Sophia Carter</h2>
              <p className="text-gray-500 text-sm">Full Name</p>
              <p className="mt-2">sophia.carter@email.com</p>
              <p className="text-gray-500 text-sm">January 15, 2023</p>
              <p className="text-gray-400 text-xs">Member Since</p>
            </div>
          </div>
          <button className="mt-6 bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600">
            Save Changes
          </button>
        </section>

        {/* Preferences */}
        <section>
          <h2 className="text-lg font-semibold mb-4">Preferences</h2>
          <div className="space-y-4">
            {[
              {
                title: "Chat Style",
                desc: "Choose your preferred style of interaction with the chatbot.",
              },
              {
                title: "Notifications",
                desc: "Manage how often you receive notifications from MineMate.",
              },
              {
                title: "Privacy Settings",
                desc: "Adjust your privacy settings to control data sharing.",
              },
            ].map((pref, idx) => (
              <div
                key={idx}
                className="flex items-center justify-between p-4 bg-white shadow rounded-lg"
              >
                <div>
                  <h3 className="font-medium">{pref.title}</h3>
                  <p className="text-sm text-gray-500">{pref.desc}</p>
                </div>
                <button className="bg-gray-100 hover:bg-gray-200 px-4 py-2 rounded-lg">
                  Edit
                </button>
              </div>
            ))}
          </div>
        </section>

        {/* Mood Stats */}
        <section>
          <h2 className="text-lg font-semibold mb-4">Mood & Activity Stats</h2>
          <div className="bg-white shadow rounded-lg p-6">
            <p className="text-3xl font-bold">75%</p>
            <p className="text-sm text-gray-500">
              Last 30 Days <span className="text-green-500">+5%</span>
            </p>
            <div className="h-48 mt-6">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={data}>
                  <XAxis dataKey="day" />
                  <YAxis hide />
                  <Tooltip />
                  <Line
                    type="monotone"
                    dataKey="mood"
                    stroke="#3b82f6"
                    strokeWidth={2}
                    dot={false}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        </section>

        {/* Actions */}
        <section>
          <h2 className="text-lg font-semibold mb-4">Additional Actions</h2>
          <div className="space-y-3">
            <button className="w-full bg-gray-100 hover:bg-gray-200 px-4 py-2 rounded-lg">
              Change Password
            </button>
            <button className="w-full bg-gray-100 hover:bg-gray-200 px-4 py-2 rounded-lg">
              Delete Account
            </button>
            <button className="w-full bg-gray-100 hover:bg-gray-200 px-4 py-2 rounded-lg">
              Connect with Professional
            </button>
          </div>
        </section>
      </main>
    </div>
  );
}
