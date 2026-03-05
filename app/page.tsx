import Link from "next/link";

type Card = {
  title: string;
  subtitle: string;
  href: string;
  icon: "factory" | "briefcase" | "bag" | "helmet";
  floatClass: string; // egyedi lebegés
};

const cards: Card[] = [
  {
    title: "Manufacturer",
    subtitle: "List products & get buyers",
    href: "/manufacturer",
    icon: "factory",
    floatClass: "animate-float1",
  },
  {
    title: "Business Buyer",
    subtitle: "Source at scale",
    href: "/business-buyer",
    icon: "briefcase",
    floatClass: "animate-float2",
  },
  {
    title: "Individual Buyer",
    subtitle: "Buy instantly",
    href: "/individual-buyer",
    icon: "bag",
    floatClass: "animate-float3",
  },
  {
    title: "Builder",
    subtitle: "Build & deploy fast",
    href: "/builder",
    icon: "helmet",
    floatClass: "animate-float4",
  },
];

function Icon({ name }: { name: Card["icon"] }) {
  // Minimal, clean, neon-ish inline SVG icons (no external deps)
  if (name === "factory") {
    return (
      <svg viewBox="0 0 24 24" className="h-10 w-10">
        <path
          d="M3 21V10l6 3V10l6 3V7l6 3v11H3Zm4-2h2v-3H7v3Zm4 0h2v-5h-2v5Zm4 0h2v-4h-2v4Z"
          className="fill-current"
        />
      </svg>
    );
  }
  if (name === "briefcase") {
    return (
      <svg viewBox="0 0 24 24" className="h-10 w-10">
        <path
          d="M10 4h4a2 2 0 0 1 2 2v2h3a2 2 0 0 1 2 2v3H1v-3a2 2 0 0 1 2-2h3V6a2 2 0 0 1 2-2Zm4 4V6h-4v2h4Zm9 8v4a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2v-4h8v1h6v-1h8Z"
          className="fill-current"
        />
      </svg>
    );
  }
  if (name === "bag") {
    return (
      <svg viewBox="0 0 24 24" className="h-10 w-10">
        <path
          d="M7 7V6a5 5 0 0 1 10 0v1h3l-1 14H5L4 7h3Zm2 0h6V6a3 3 0 0 0-6 0v1Z"
          className="fill-current"
        />
      </svg>
    );
  }
  // helmet
  return (
    <svg viewBox="0 0 24 24" className="h-10 w-10">
      <path
        d="M12 3a9 9 0 0 0-9 9v6h18v-6a9 9 0 0 0-9-9Zm7 13H5v-4h14v4ZM5 10.5A7 7 0 0 1 19 10.5V12H5v-1.5Z"
        className="fill-current"
      />
    </svg>
  );
}

function NeonCard({ card }: { card: Card }) {
  return (
    <Link
      href={card.href}
      className={[
        "group relative block w-[290px] max-w-[86vw]",
        card.floatClass,
      ].join(" ")}
    >
      {/* glow ring behind */}
      <div
        className="pointer-events-none absolute -inset-6 opacity-70 blur-2xl transition-opacity duration-300 group-hover:opacity-100"
        style={{
          background:
            "radial-gradient(closest-side, rgba(34,211,238,0.35), transparent 70%)",
        }}
      />

      <div className="relative overflow-hidden rounded-2xl border border-cyan-300/20 bg-white/[0.05] p-6 shadow-[0_20px_60px_rgba(0,0,0,0.55)] backdrop-blur-md transition-all duration-300 group-hover:-translate-y-1 group-hover:scale-[1.035] group-hover:border-cyan-300/45 group-hover:bg-white/[0.09]">
        {/* inner sheen */}
        <div className="pointer-events-none absolute inset-0 opacity-0 transition-opacity duration-300 group-hover:opacity-100">
          <div
            className="absolute -top-24 left-1/2 h-48 w-[520px] -translate-x-1/2 rotate-12"
            style={{
              background:
                "linear-gradient(90deg, transparent, rgba(34,211,238,0.18), transparent)",
            }}
          />
        </div>

        <div className="flex items-center gap-4">
          <div className="grid h-14 w-14 place-items-center rounded-xl border border-cyan-300/25 bg-cyan-300/10 text-cyan-200 shadow-[0_0_35px_rgba(34,211,238,0.18)] transition-all duration-300 group-hover:shadow-[0_0_55px_rgba(34,211,238,0.32)]">
            <Icon name={card.icon} />
          </div>

          <div className="min-w-0">
            <div className="text-lg font-semibold tracking-wide text-cyan-100">
              {card.title}
            </div>
            <div className="mt-1 text-sm text-white/60">{card.subtitle}</div>
          </div>
        </div>

        {/* bottom neon line */}
        <div className="mt-5 h-px w-full bg-gradient-to-r from-transparent via-cyan-300/50 to-transparent opacity-70" />

        {/* small hint */}
        <div className="mt-4 flex items-center justify-between text-xs text-white/55">
          <span>Enter</span>
          <span className="translate-x-0 transition-transform duration-300 group-hover:translate-x-1">
            →
          </span>
        </div>
      </div>
    </Link>
  );
}

export default function Page() {
  return (
    <main className="relative min-h-screen overflow-hidden bg-[#05060b] text-white">
      {/* BACKGROUND LAYERS */}
      {/* base vignette */}
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(70%_55%_at_50%_35%,rgba(34,211,238,0.10),transparent_60%),radial-gradient(55%_45%_at_20%_65%,rgba(59,130,246,0.10),transparent_55%),radial-gradient(60%_50%_at_80%_70%,rgba(34,211,238,0.08),transparent_55%)]" />

      {/* grid floor */}
      <div className="pointer-events-none absolute inset-0 opacity-[0.22]">
        <div className="absolute inset-x-0 bottom-0 top-[45%] [transform:perspective(900px)_rotateX(60deg)]">
          <div
            className="h-full w-full"
            style={{
              backgroundImage:
                "linear-gradient(to right, rgba(34,211,238,0.25) 1px, transparent 1px), linear-gradient(to top, rgba(34,211,238,0.22) 1px, transparent 1px)",
              backgroundSize: "48px 48px",
              maskImage:
                "linear-gradient(to top, rgba(0,0,0,1), rgba(0,0,0,0))",
              WebkitMaskImage:
                "linear-gradient(to top, rgba(0,0,0,1), rgba(0,0,0,0))",
            }}
          />
        </div>
      </div>

      {/* skyline lines */}
      <div className="pointer-events-none absolute inset-0 opacity-[0.55]">
        <svg
          className="absolute left-8 top-28 hidden md:block"
          width="420"
          height="220"
          viewBox="0 0 420 220"
          fill="none"
        >
          <path
            d="M30 200V140M60 200V120M95 200V90M130 200V70M170 200V110M205 200V85M240 200V130M280 200V75M320 200V105M360 200V135"
            stroke="rgba(34,211,238,0.35)"
            strokeWidth="2"
          />
          <text x="10" y="80" fill="rgba(34,211,238,0.55)" fontSize="14">
            Energy
          </text>
          <text x="150" y="55" fill="rgba(34,211,238,0.55)" fontSize="14">
            Manufacturing
          </text>
        </svg>

        {/* gears arcs */}
        <svg
          className="absolute right-[-80px] top-[-60px] opacity-70"
          width="560"
          height="560"
          viewBox="0 0 560 560"
          fill="none"
        >
          <circle
            cx="320"
            cy="260"
            r="170"
            stroke="rgba(34,211,238,0.22)"
            strokeWidth="2"
          />
          <circle
            cx="320"
            cy="260"
            r="210"
            stroke="rgba(34,211,238,0.14)"
            strokeWidth="2"
            strokeDasharray="8 10"
          />
          <path
            d="M490 250c0 95-77 172-172 172"
            stroke="rgba(34,211,238,0.30)"
            strokeWidth="3"
          />
        </svg>
      </div>

      {/* CONTENT */}
      <section className="relative mx-auto flex min-h-screen max-w-6xl flex-col items-center justify-center px-6 py-16">
        {/* Title */}
        <div className="text-center">
          <h1 className="text-4xl font-extrabold tracking-[0.18em] text-cyan-300 md:text-6xl">
            SMARTARTAI NEXUS
          </h1>
          <p className="mt-4 text-lg text-white/75 md:text-xl">
            Global Intelligence Platform
          </p>
          <p className="mt-2 text-sm tracking-widest text-white/60">
            Find. Build. Buy. Instantly.
          </p>
        </div>

        {/* "Tablet" base */}
        <div className="relative mt-12 w-full max-w-3xl">
          {/* tablet glow */}
          <div
            className="pointer-events-none absolute left-1/2 top-10 h-[420px] w-[520px] -translate-x-1/2 rounded-[48px] opacity-70 blur-3xl"
            style={{
              background:
                "radial-gradient(closest-side, rgba(34,211,238,0.25), transparent 70%)",
            }}
          />

          {/* tablet body */}
          <div className="relative mx-auto h-[520px] w-full rounded-[48px] border border-cyan-300/20 bg-white/[0.04] shadow-[0_40px_140px_rgba(0,0,0,0.65)] backdrop-blur-md">
            {/* tablet frame highlight */}
            <div className="pointer-events-none absolute inset-0 rounded-[48px] ring-1 ring-white/5" />
            <div className="pointer-events-none absolute inset-x-10 top-6 h-px bg-gradient-to-r from-transparent via-cyan-300/40 to-transparent" />

            {/* floating cards layout */}
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="relative h-full w-full">
                {/* positions */}
                <div className="absolute left-1/2 top-[16%] -translate-x-1/2">
                  <NeonCard card={cards[0]} />
                </div>

                <div className="absolute left-[58%] top-[33%] -translate-x-1/2">
                  <NeonCard card={cards[1]} />
                </div>

                <div className="absolute left-[42%] top-[52%] -translate-x-1/2">
                  <NeonCard card={cards[2]} />
                </div>

                <div className="absolute left-1/2 top-[70%] -translate-x-1/2">
                  <NeonCard card={cards[3]} />
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Footer note */}
        <div className="mt-10 text-center text-sm text-white/55">
          Launching Soon — Stay Tuned
        </div>
      </section>

      {/* Page-local animations */}
      <style jsx global>{`
        @keyframes floatA {
          0%,
          100% {
            transform: translate3d(0, 0, 0);
          }
          50% {
            transform: translate3d(0, -10px, 0);
          }
        }
        @keyframes floatB {
          0%,
          100% {
            transform: translate3d(0, 0, 0);
          }
          50% {
            transform: translate3d(0, -14px, 0);
          }
        }
        @keyframes floatC {
          0%,
          100% {
            transform: translate3d(0, 0, 0);
          }
          50% {
            transform: translate3d(0, -8px, 0);
          }
        }
        @keyframes floatD {
          0%,
          100% {
            transform: translate3d(0, 0, 0);
          }
          50% {
            transform: translate3d(0, -12px, 0);
          }
        }

        .animate-float1 {
          animation: floatA 5.2s ease-in-out infinite;
        }
        .animate-float2 {
          animation: floatB 6.0s ease-in-out infinite;
        }
        .animate-float3 {
          animation: floatC 5.6s ease-in-out infinite;
        }
        .animate-float4 {
          animation: floatD 6.4s ease-in-out infinite;
        }
      `}</style>
    </main>
  );
}
