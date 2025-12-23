import { useMemo } from "react";

type Props = {
  icon: string;
  title: string;
  text: string;
  tone?: "primary" | "purple" | "blue";
};

export default function Benefit({ icon, title, text, tone = "primary" }: Props) {
  const toneCls = useMemo(() => {
    if (tone === "purple") return "bg-purple-100 text-[#7A00D2]";
    if (tone === "blue") return "bg-blue-100 text-blue-600";
    return "bg-[#23C062]/10 text-[#23C062]";
  }, [tone]);

  return (
    <div className="flex items-start gap-4">
      <div className={`p-2 rounded-lg ${toneCls}`}>
        <span className="material-symbols-outlined">{icon}</span>
      </div>
      <div>
        <h4 className="font-bold text-[#0F1A13]">{title}</h4>
        <p className="text-sm text-[#54926D] mt-1 leading-relaxed">{text}</p>
      </div>
    </div>
  );
}
