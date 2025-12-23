import logo from "../../assets/Logo Partido Oxígeno CNE_1.png";

export default function Navbar() {
  return (
    <header className="sticky top-0 z-50">
      <div className="bg-transparent backdrop-blur-[6px]">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <img src={logo} alt="Oxígeno" className="h-14 w-auto" />
          </div>

          <button
            className="
              hidden sm:inline-flex items-center justify-center
              h-10 px-6 rounded-full
              bg-gradient-to-r from-[#23C062] to-[#7A00D2]
              text-white font-semibold text-sm
              shadow-sm hover:shadow-md
              transition
            "
            type="button"
          >
            Donar
          </button>

          <button
            className="sm:hidden text-[#0F1A13]"
            type="button"
            aria-label="Menú"
          >
            <span className="material-symbols-outlined">menu</span>
          </button>
        </div>
      </div>
    </header>
  );
}
