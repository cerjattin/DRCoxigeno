import Benefit from "../ui/Benefit";
import InputField from "../ui/InputField";
import SelectField from "../ui/SelectField";

export default function RegisterForm() {
  return (
    <div className="bg-white/70 rounded-2xl border border-white/60 shadow-[0_20px_60px_rgba(0,0,0,0.10)] overflow-hidden">
      <div className="grid grid-cols-1 md:grid-cols-3">
        {/* Form */}
        <div className="md:col-span-2 p-6 md:p-10 lg:p-12">
          <div className="flex items-center gap-2 mb-6">
            <span className="material-symbols-outlined text-transparent bg-clip-text bg-gradient-to-br from-[#23C062] to-[#7A00D2]">
              app_registration
            </span>
            <h3 className="text-xl font-bold">Regístrate ahora</h3>
          </div>

          <form className="flex flex-col gap-5">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              <InputField
                label="Nombres"
                icon="person"
                name="first_name"
                placeholder="Juan"
              />
              <InputField
                label="Apellidos"
                icon="badge"
                name="last_name"
                placeholder="Pérez"
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              <InputField
                label="Documento de Identidad"
                icon="branding_watermark"
                name="document"
                placeholder="123456789"
                type="text"
                inputMode="numeric"
                pattern="[0-9]*"
              />
              <InputField
                label="Teléfono / Celular"
                icon="smartphone"
                name="phone"
                placeholder="3001234567"
                type="tel"
                inputMode="numeric"
                pattern="[0-9+ ]*"
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              <SelectField
                label="Líder"
                icon="diversity_3"
                name="leader_id"
                placeholder="Selecciona un líder"
                options={[
                  { value: "1", label: "Líder Zona Norte" },
                  { value: "2", label: "Líder Zona Sur" },
                ]}
              />
              <SelectField
                label="Coordinador"
                icon="manage_accounts"
                name="coordinator_id"
                placeholder="Selecciona un coordinador"
                options={[
                  { value: "1", label: "Coordinador General" },
                  { value: "2", label: "Coordinador de Territorio" },
                ]}
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              <SelectField
                label="Ciudad / Municipio"
                icon="location_city"
                name="municipality_id"
                placeholder="Selecciona tu ciudad"
                options={[
                  { value: "1", label: "Barranquilla" },
                  { value: "2", label: "Soledad" },
                ]}
              />
              <SelectField
                label="Barrio"
                icon="holiday_village"
                name="neighborhood_id"
                placeholder="Selecciona tu barrio"
                options={[
                  { value: "10", label: "Centro" },
                  { value: "11", label: "Riomar" },
                ]}
              />
            </div>

            <InputField
              label="Dirección de Residencia"
              icon="home_pin"
              name="address"
              placeholder="Calle 123 # 45 - 67"
            />

            <div className="flex items-start gap-3 mt-2">
              <input
                className="mt-1 h-5 w-5 rounded border-gray-300 text-[#23C062] focus:ring-[#23C062]"
                id="consent"
                name="consent"
                type="checkbox"
                required
              />
              <label htmlFor="consent" className="text-sm text-[#54926D] leading-6">
                Acepto la{" "}
                <a
                  className="font-semibold text-[#23C062] hover:text-[#7A00D2] hover:underline transition"
                  href="#"
                >
                  política de tratamiento de datos personales
                </a>
                . Entiendo que mis datos serán usados para fines de comunicación política del
                movimiento Oxígeno.
              </label>
            </div>

            <button
              type="submit"
              className="
                mt-4 w-full inline-flex items-center justify-center gap-2
                rounded-xl py-4 px-5
                text-base font-bold text-white
                bg-gradient-to-r from-[#23C062] to-[#23C062]
                shadow-md hover:shadow-lg
                transition active:scale-[0.99]
              "
            >
              Quiero ser parte
              <span className="material-symbols-outlined">arrow_forward</span>
            </button>
          </form>
        </div>

        {/* Side benefits */}
        <aside className="hidden md:flex md:col-span-1 p-10 border-l border-[#D2E5D9]/30 bg-white/25 relative">
          <div className="absolute inset-0 opacity-15 bg-[radial-gradient(circle_at_top_right,_var(--tw-gradient-stops))] from-[#23C062] via-[#7A00D2] to-transparent" />
          <div className="relative z-10 flex flex-col gap-6">
            <Benefit
              icon="verified_user"
              title="Datos Seguros"
              text="Tus datos están protegidos. Cumplimos con la ley de protección de datos."
              tone="primary"
            />
            <Benefit
              icon="rocket_launch"
              title="Impacto Real"
              text="Al registrarte, tu información ayuda a organizar y fortalecer comunidades locales."
              tone="purple"
            />
            <Benefit
              icon="groups"
              title="Comunidad Activa"
              text="Únete a miles de personas que están trabajando activamente para hacer un gran cambio."
              tone="blue"
            />

            <div className="mt-6 rounded-xl overflow-hidden h-40 bg-gray-100 relative">
              <div className="absolute inset-0 bg-gradient-to-t from-white/60 to-transparent" />
              <div className="h-full w-full bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-[#23C062]/20 via-[#7A00D2]/10 to-transparent" />
            </div>

            <p className="text-xs text-center text-[#54926D]/70">
              Juntos somos más fuertes.
            </p>
          </div>
        </aside>
      </div>
    </div>
  );
}
