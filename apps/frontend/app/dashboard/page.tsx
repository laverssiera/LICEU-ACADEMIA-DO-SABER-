"use client";

import { motion } from "framer-motion";

export default function DashboardPage() {
  return (
    <div className="min-h-screen bg-black text-white">
      <div className="grid grid-cols-5 gap-4 p-6">
        <motion.div whileHover={{ scale: 1.03 }} className="bg-zinc-900 p-5 rounded-2xl">
          <h1 className="text-sm text-zinc-400">Students Online</h1>
          <p className="text-5xl font-bold mt-2">14,882</p>
        </motion.div>
        <motion.div whileHover={{ scale: 1.03 }} className="bg-zinc-900 p-5 rounded-2xl">
          <h1 className="text-sm text-zinc-400">Simulations</h1>
          <p className="text-5xl font-bold mt-2">212</p>
        </motion.div>
      </div>
    </div>
  );
}
