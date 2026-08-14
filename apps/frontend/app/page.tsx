export default function HomePage() {
  return (
    <main className="bg-black text-white">
      <section className="min-h-screen flex items-center justify-center">
        <div className="text-center max-w-5xl">
          <h1 className="text-7xl font-bold">LICEU Academia do Saber</h1>
          <p className="text-2xl mt-8 text-zinc-400">
            Educacao cognitiva viva, holografica, adaptativa e integrada ao mundo real.
          </p>
          <div className="flex justify-center gap-4 mt-10">
            <button className="bg-white text-black px-6 py-4 rounded-xl">Iniciar Jornada</button>
            <button className="border border-white px-6 py-4 rounded-xl">Conhecer Campus</button>
          </div>
        </div>
      </section>
    </main>
  );
}
