type Props = {
  label: string;
  icon: string;
  name: string;
  placeholder: string;
  type?: string;
  inputMode?: React.HTMLAttributes<HTMLInputElement>["inputMode"];
  pattern?: string;
};

export default function InputField({
  label,
  icon,
  name,
  placeholder,
  type = "text",
  inputMode,
  pattern,
}: Props) {
  return (
    <label className="flex flex-col">
      <span className="text-sm font-medium text-[#0F1A13] mb-2">{label}</span>
      <div className="relative group">
        <span className="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-[#54926D] text-[20px]">
          {icon}
        </span>
        <input
          name={name}
          required
          type={type}
          inputMode={inputMode}
          pattern={pattern}
          placeholder={placeholder}
          className="
            w-full h-12 md:h-14
            rounded-xl border border-[#D2E5D9]
            bg-white/70
            pl-11 pr-4
            text-[#0F1A13] placeholder:text-[#54926D]/60
            focus:outline-none focus:ring-2 focus:ring-[#7A00D2]/20 focus:border-[#7A00D2]
            transition
          "
        />
      </div>
    </label>
  );
}
