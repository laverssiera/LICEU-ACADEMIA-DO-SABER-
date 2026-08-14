import React from "react";

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-black text-white p-6">
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
        <div className="bg-zinc-900 p-4 rounded">
          <h1 className="text-xl">Students Online</h1>
          <p className="text-5xl font-bold">14,882</p>
        </div>
        <div className="bg-zinc-900 p-4 rounded">
          <h1 className="text-xl">Active Simulations</h1>
          <p className="text-5xl font-bold">512</p>
        </div>
        <div className="bg-zinc-900 p-4 rounded">
          <h1 className="text-xl">Holographic Rooms</h1>
          <p className="text-5xl font-bold">128</p>
        </div>
        <div className="bg-zinc-900 p-4 rounded">
          <h1 className="text-xl">AI Learning Accuracy</h1>
          <p className="text-5xl font-bold">97%</p>
        </div>
      </div>
    </div>
  );
}
