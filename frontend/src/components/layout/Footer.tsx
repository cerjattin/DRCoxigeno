import logo from "../../assets/Logo Partido Oxígeno CNE_1.png";

export default function Footer() {
  return (
    <footer className="mt-10 border-t border-[#D2E5D9]/60 bg-white/40 backdrop-blur-sm">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 py-8 flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-2">
          <img src={logo} alt="Oxígeno" className="h-7 w-auto" />
          <span className="font-bold text-sm text-[#0F1A13]">
            David Reyes C © 2026
          </span>
        </div>

        <div className="flex gap-6 text-sm text-[#54926D]">
          <a className="hover:text-[#23C062] transition" href="#">
            Política de Privacidad
          </a>
          <a className="hover:text-[#23C062] transition" href="#">
            Términos y Condiciones
          </a>
          <a className="hover:text-[#23C062] transition" href="#">
            Contacto
          </a>
        </div>
      </div>
    </footer>
  );
}
