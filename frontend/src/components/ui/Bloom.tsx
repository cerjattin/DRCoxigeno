export default function Bloom({ className }: { className: string }) {
  return (
    <div
      className={[
        "absolute -z-10 rounded-full blur-[120px] opacity-40",
        className,
      ].join(" ")}
    />
  );
}
