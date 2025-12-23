type Props = {
  label: string;
  icon: string;
  name: string;
  placeholder: string;
  options: { value: string; label: string }[];
};

export default function SelectField({
  label,
  icon,
  name,
  placeholder,
  options,
}: Props) {
  return (
    <label className="flex flex-col">
      <span className="text-sm font-medium text-[#0F1A13] mb-2">{label}</span>

      <div className="relative">
        <span className="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-[#54926D] text-[20px]">
          {icon}
        </span>

        <select
          name={name}
          required
          defaultValue=""
          className="
            w-full h-12 md:h-14
            rounded-xl border border-[#D2E5D9]
            bg-white/70
            pl-11 pr-10
            text-[#0F1A13]
            focus:outline-none focus:ring-2 focus:ring-[#7A00D2]/20 focus:border-[#7A00D2]
            transition appearance-none
          "
        >
          <option value="" disabled>
            {placeholder}
          </option>
          {options.map((o) => (
            <option key={o.value} value={o.value}>
              {o.label}
            </option>
          ))}
        </select>

        <span className="material-symbols-outlined absolute right-3 top-1/2 -translate-y-1/2 text-[#54926D]">
          expand_more
        </span>
      </div>
    </label>
  );
}
