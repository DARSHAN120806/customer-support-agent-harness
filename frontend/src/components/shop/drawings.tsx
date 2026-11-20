// The drawings themselves, one per product slug. Kept apart from ProductArt.tsx
// so that file holds only the component.
import type { ReactNode } from 'react'

const SHADOW = 'rgba(31, 27, 22, 0.10)'

// The soft shadow under each product.
function floor(width = 60) {
  return <ellipse cx="100" cy="140" rx={width} ry="6" fill={SHADOW} />
}

export const DRAWINGS: Record<string, ReactNode> = {
  'bluetooth-speaker-mini': (
    <>
      {floor(52)}
      <rect x="56" y="58" width="88" height="80" rx="20" fill="#4b5056" />
      <rect x="64" y="66" width="72" height="54" rx="12" fill="#3d4146" />
      {Array.from({ length: 24 }, (_, i) => (
        <circle key={i} cx={74 + (i % 6) * 10.4} cy={76 + Math.floor(i / 6) * 11} r="1.8" fill="#5a5f65" />
      ))}
      <rect x="92" y="126" width="16" height="4" rx="2" fill="#5a5f65" />
      <path d="M144 76 Q158 80 156 96" stroke="#3d4146" strokeWidth="4" fill="none" strokeLinecap="round" />
    </>
  ),
  'wireless-earbuds-pro': (
    <>
      {floor(48)}
      <rect x="62" y="74" width="76" height="62" rx="28" fill="#f6f4ef" stroke="rgba(31,27,22,0.12)" />
      <path d="M64 96 H136" stroke="rgba(31,27,22,0.14)" />
      <circle cx="100" cy="114" r="2.5" fill="#6b8f71" />
      <circle cx="150" cy="122" r="11" fill="#f6f4ef" stroke="rgba(31,27,22,0.12)" />
      <rect x="146" y="104" width="7" height="16" rx="3.5" fill="#f6f4ef" stroke="rgba(31,27,22,0.12)" />
    </>
  ),
  'led-desk-lamp': (
    <>
      {floor(40)}
      <rect x="62" y="128" width="56" height="10" rx="5" fill="#2f3336" />
      <path d="M90 128 L104 80 L136 62" stroke="#2f3336" strokeWidth="6" fill="none" strokeLinecap="round" strokeLinejoin="round" />
      <circle cx="104" cy="80" r="5" fill="#45494d" />
      <path d="M128 52 L162 66 L156 80 L122 66 Z" fill="#2f3336" />
      <path d="M124 68 L156 81" stroke="#f3ead2" strokeWidth="3" strokeLinecap="round" />
    </>
  ),
  'electric-kettle-1-7l': (
    <>
      {floor(44)}
      <path d="M126 70 Q152 72 148 100 Q145 122 128 124" stroke="#2b2d30" strokeWidth="7" fill="none" strokeLinecap="round" />
      <path d="M72 70 L58 60 L60 70 L74 82 Z" fill="#b3b9be" />
      <path d="M70 134 L76 64 Q100 56 124 64 L130 134 Z" fill="#c3c8cd" />
      <path d="M112 62 Q120 63 124 64 L130 134 L116 134 Z" fill="#b1b7bd" />
      <rect x="84" y="84" width="6" height="38" rx="3" fill="#9ea5ac" />
      <ellipse cx="100" cy="61" rx="22" ry="4" fill="#a9afb5" />
      <rect x="95" y="52" width="10" height="7" rx="3" fill="#2b2d30" />
      <rect x="66" y="130" width="68" height="9" rx="3" fill="#2b2d30" />
    </>
  ),
  'smart-plug-2-pack': (
    <>
      {floor(58)}
      {[52, 104].map((x) => (
        <g key={x}>
          <rect x={x} y="74" width="46" height="62" rx="12" fill="#f6f4ef" stroke="rgba(31,27,22,0.12)" />
          <rect x={x + 14} y="94" width="4" height="12" rx="2" fill="#b9b2a6" />
          <rect x={x + 28} y="94" width="4" height="12" rx="2" fill="#b9b2a6" />
          <circle cx={x + 23} cy="120" r="2.5" fill="#6b8f71" />
        </g>
      ))}
    </>
  ),
  'oak-side-table': (
    <>
      {floor(56)}
      <rect x="58" y="76" width="8" height="62" rx="2" fill="#b38959" />
      <rect x="134" y="76" width="8" height="62" rx="2" fill="#b38959" />
      <rect x="62" y="112" width="76" height="6" rx="2" fill="#b38959" />
      <rect x="48" y="62" width="104" height="10" rx="3" fill="#c9a06f" />
      <rect x="48" y="72" width="104" height="5" rx="2" fill="#a97f52" />
      <path d="M60 66 H100 M108 67 H142" stroke="#b38959" strokeWidth="1" />
    </>
  ),
  'wool-throw-blanket': (
    <>
      {floor(58)}
      <rect x="46" y="108" width="108" height="26" rx="10" fill="#b9a585" />
      <rect x="52" y="86" width="96" height="26" rx="10" fill="#cbb999" />
      {[70, 86, 102, 118, 134].map((x) => (
        <path key={x} d={`M${x} 88 V110 M${x - 4} 110 V132`} stroke="#a8936f" strokeWidth="2" />
      ))}
      {[90, 96, 102, 108].map((y) => (
        <path key={y} d={`M52 ${y + 2} H45`} stroke="#b9a585" strokeWidth="2" strokeLinecap="round" />
      ))}
    </>
  ),
  'cast-iron-skillet': (
    <>
      {floor(58)}
      <path d="M128 106 L172 94 Q179 93 178 100 L132 116 Z" fill="#363432" />
      <circle cx="171" cy="98" r="2.5" fill="#efe9df" />
      <ellipse cx="88" cy="118" rx="46" ry="16" fill="#2b2927" />
      <ellipse cx="88" cy="110" rx="46" ry="16" fill="#3a3836" />
      <ellipse cx="88" cy="111" rx="38" ry="12" fill="#2b2927" />
    </>
  ),
  'ceramic-pour-over-coffee-set': (
    <>
      {floor(60)}
      <path d="M66 100 Q64 136 74 138 L106 138 Q116 136 114 100 Z" fill="#d6cbb8" />
      <rect x="70" y="96" width="40" height="8" rx="3" fill="#c4b8a2" />
      <path d="M66 66 L114 66 L102 96 L78 96 Z" fill="#f7f3ec" stroke="rgba(31,27,22,0.12)" />
      <path d="M78 74 L84 92 M90 74 L90 92 M102 74 L96 92" stroke="#d9d1c2" strokeWidth="1.5" />
      <rect x="62" y="62" width="56" height="6" rx="3" fill="#d6cbb8" />
      <rect x="124" y="110" width="30" height="28" rx="6" fill="#f7f3ec" stroke="rgba(31,27,22,0.12)" />
      <path d="M154 116 Q164 118 162 126 Q160 132 154 132" stroke="#d6cbb8" strokeWidth="5" fill="none" />
      <ellipse cx="139" cy="111" rx="13" ry="2.5" fill="#5b4334" />
    </>
  ),
  'ceramic-planter-set': (
    <>
      {floor(64)}
      <path d="M86 84 Q78 64 92 52 Q96 70 90 84 Z" fill="#6b8f71" />
      <path d="M96 84 Q104 60 118 58 Q110 74 100 84 Z" fill="#5b7d61" />
      <path d="M78 86 L122 86 L116 138 L84 138 Z" fill="#c9765a" />
      <rect x="76" y="82" width="48" height="8" rx="3" fill="#b8684d" />
      <path d="M44 106 Q40 90 50 86 Q54 98 50 106 Z" fill="#6b8f71" />
      <path d="M38 108 L68 108 L64 138 L42 138 Z" fill="#d7a184" />
      <path d="M150 104 Q156 88 166 90 Q160 100 154 106 Z" fill="#5b7d61" />
      <path d="M134 108 L168 108 L164 138 L138 138 Z" fill="#e2cdb6" />
    </>
  ),
  'bamboo-cutting-board': (
    <>
      {floor(58)}
      <rect x="44" y="72" width="112" height="64" rx="10" fill="#d8b878" />
      {[60, 76, 92, 108, 124, 140].map((x) => (
        <path key={x} d={`M${x} 74 V134`} stroke="#c8a763" strokeWidth="1.5" />
      ))}
      <rect x="144" y="94" width="18" height="20" rx="6" fill="#d8b878" />
      <circle cx="154" cy="104" r="4" fill="#efe9df" />
    </>
  ),
  'linen-napkins-set-of-4': (
    <>
      {floor(56)}
      <rect x="50" y="110" width="100" height="26" rx="4" fill="#b8ab90" />
      <rect x="54" y="96" width="92" height="18" rx="4" fill="#cbbfa6" />
      <rect x="58" y="82" width="84" height="18" rx="4" fill="#ddd3be" />
      <path d="M58 92 H142 M54 106 H146 M50 122 H150" stroke="rgba(31,27,22,0.08)" />
      <path d="M100 82 V100" stroke="rgba(31,27,22,0.10)" />
    </>
  ),
  'adjustable-phone-stand': (
    <>
      {floor(46)}
      <path d="M86 130 L108 76 L116 78 L96 130 Z" fill="#a9aeb3" />
      <rect x="58" y="128" width="84" height="9" rx="4" fill="#bdc1c5" />
      <g transform="rotate(20 104 96)">
        <rect x="84" y="52" width="42" height="80" rx="9" fill="#2b2d30" />
        <rect x="88" y="58" width="34" height="68" rx="5" fill="#3d4247" />
      </g>
      <rect x="74" y="122" width="28" height="6" rx="3" fill="#a9aeb3" />
    </>
  ),
  'scented-soy-candle': (
    <>
      {floor(36)}
      <rect x="72" y="76" width="56" height="62" rx="8" fill="#b9773a" />
      <rect x="72" y="76" width="12" height="62" rx="6" fill="#a96a30" />
      <rect x="82" y="98" width="38" height="22" rx="2" fill="#f3ece0" />
      <path d="M88 106 H114 M92 112 H110" stroke="#c7bba8" strokeWidth="2" strokeLinecap="round" />
      <ellipse cx="100" cy="78" rx="26" ry="5" fill="#f1e9d8" />
      <path d="M100 78 V68" stroke="#3a3836" strokeWidth="2" strokeLinecap="round" />
    </>
  ),
  'personalised-leather-notebook': (
    <>
      {floor(44)}
      <rect x="62" y="54" width="78" height="84" rx="6" fill="#7a4a2e" />
      <rect x="62" y="54" width="12" height="84" rx="5" fill="#683e25" />
      <rect x="126" y="54" width="5" height="84" fill="#4a2c1b" />
      <rect x="86" y="88" width="28" height="3" rx="1.5" fill="#683e25" />
      <rect x="92" y="96" width="16" height="3" rx="1.5" fill="#683e25" />
      <path d="M140 60 V132" stroke="#efe6d6" strokeWidth="2" />
    </>
  ),
  'juniper-lane-gift-card': (
    <>
      {floor(56)}
      <g transform="rotate(-6 100 100)">
        <rect x="44" y="64" width="112" height="70" rx="8" fill="#2f5d4e" />
        <text x="56" y="84" fill="#f7f4ee" fontSize="9" fontWeight="500" fontFamily="Instrument Sans, sans-serif">
          Juniper Lane Goods
        </text>
        <text x="56" y="122" fill="#c9d8d1" fontSize="8" fontFamily="IBM Plex Mono, monospace">
          Gift card
        </text>
        <circle cx="140" cy="116" r="6" fill="none" stroke="#c9d8d1" strokeWidth="1.5" />
      </g>
    </>
  ),
}

export const DRAWN_PRODUCTS = Object.keys(DRAWINGS)
