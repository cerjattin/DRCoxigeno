import WatermarkTiled from "../components/layout/WatermarkTiled";
import Navbar from "../components/layout/Navbar";
import Footer from "../components/layout/Footer";
import RegisterForm from "../components/register/RegisterForm";

export default function RegisterPage() {
  return (
    <div className="min-h-screen text-[#0F1A13] font-sans">
      <WatermarkTiled />
      <Navbar />

      <main className="mx-auto max-w-7xl px-4 sm:px-6 py-10">
        <section className="text-center mt-4 md:mt-10">
          <p className="mt-4 text-lg md:text-xl text-[#54926D] max-w-2xl mx-auto">
            Regístrate y sé parte del movimiento que transforma el país con transparencia,
            tecnología y acción ciudadana real.
          </p>
        </section>

        <section className="mt-10">
          <RegisterForm />
        </section>
      </main>

      <Footer />
    </div>
  );
}
