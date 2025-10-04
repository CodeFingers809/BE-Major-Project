// SVG outlines for face shapes on white background

export const faceShapes = {
  oval: `<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
    <rect width="200" height="240" fill="white"/>
    <ellipse cx="100" cy="120" rx="70" ry="95" fill="none" stroke="black" stroke-width="2"/>
  </svg>`,

  round: `<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
    <rect width="200" height="240" fill="white"/>
    <circle cx="100" cy="120" r="85" fill="none" stroke="black" stroke-width="2"/>
  </svg>`,

  square: `<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
    <rect width="200" height="240" fill="white"/>
    <rect x="30" y="40" width="140" height="160" rx="10" fill="none" stroke="black" stroke-width="2"/>
  </svg>`,

  diamond: `<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
    <rect width="200" height="240" fill="white"/>
    <path d="M 100 30 L 160 120 L 100 210 L 40 120 Z" fill="none" stroke="black" stroke-width="2"/>
  </svg>`,

  heart: `<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
    <rect width="200" height="240" fill="white"/>
    <path d="M 60 60 Q 60 30 80 30 Q 100 30 100 50 Q 100 30 120 30 Q 140 30 140 60 Q 140 80 100 210 Q 60 80 60 60 Z" fill="none" stroke="black" stroke-width="2"/>
  </svg>`,

  oblong: `<svg viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg">
    <rect width="200" height="240" fill="white"/>
    <ellipse cx="100" cy="120" rx="60" ry="100" fill="none" stroke="black" stroke-width="2"/>
  </svg>`
};

export const eyeShapes = {
  almond: `<svg viewBox="0 0 200 100" xmlns="http://www.w3.org/2000/svg">
    <rect width="200" height="100" fill="white"/>
    <ellipse cx="60" cy="50" rx="25" ry="12" fill="none" stroke="black" stroke-width="2"/>
    <circle cx="60" cy="50" r="5" fill="black"/>
    <ellipse cx="140" cy="50" rx="25" ry="12" fill="none" stroke="black" stroke-width="2"/>
    <circle cx="140" cy="50" r="5" fill="black"/>
  </svg>`,

  round: `<svg viewBox="0 0 200 100" xmlns="http://www.w3.org/2000/svg">
    <rect width="200" height="100" fill="white"/>
    <circle cx="60" cy="50" r="18" fill="none" stroke="black" stroke-width="2"/>
    <circle cx="60" cy="50" r="5" fill="black"/>
    <circle cx="140" cy="50" r="18" fill="none" stroke="black" stroke-width="2"/>
    <circle cx="140" cy="50" r="5" fill="black"/>
  </svg>`,

  hooded: `<svg viewBox="0 0 200 100" xmlns="http://www.w3.org/2000/svg">
    <rect width="200" height="100" fill="white"/>
    <path d="M 35 45 Q 60 35 85 45" fill="none" stroke="black" stroke-width="2"/>
    <ellipse cx="60" cy="55" rx="25" ry="10" fill="none" stroke="black" stroke-width="2"/>
    <circle cx="60" cy="55" r="5" fill="black"/>
    <path d="M 115 45 Q 140 35 165 45" fill="none" stroke="black" stroke-width="2"/>
    <ellipse cx="140" cy="55" rx="25" ry="10" fill="none" stroke="black" stroke-width="2"/>
    <circle cx="140" cy="55" r="5" fill="black"/>
  </svg>`,

  upturned: `<svg viewBox="0 0 200 100" xmlns="http://www.w3.org/2000/svg">
    <rect width="200" height="100" fill="white"/>
    <path d="M 35 55 Q 60 40 85 50" fill="none" stroke="black" stroke-width="2"/>
    <circle cx="60" cy="50" r="5" fill="black"/>
    <path d="M 115 50 Q 140 40 165 55" fill="none" stroke="black" stroke-width="2"/>
    <circle cx="140" cy="50" r="5" fill="black"/>
  </svg>`,

  downturned: `<svg viewBox="0 0 200 100" xmlns="http://www.w3.org/2000/svg">
    <rect width="200" height="100" fill="white"/>
    <path d="M 35 45 Q 60 55 85 50" fill="none" stroke="black" stroke-width="2"/>
    <circle cx="60" cy="50" r="5" fill="black"/>
    <path d="M 115 50 Q 140 55 165 45" fill="none" stroke="black" stroke-width="2"/>
    <circle cx="140" cy="50" r="5" fill="black"/>
  </svg>`,

  monolid: `<svg viewBox="0 0 200 100" xmlns="http://www.w3.org/2000/svg">
    <rect width="200" height="100" fill="white"/>
    <line x1="35" y1="50" x2="85" y2="50" stroke="black" stroke-width="2"/>
    <circle cx="60" cy="50" r="5" fill="black"/>
    <line x1="115" y1="50" x2="165" y2="50" stroke="black" stroke-width="2"/>
    <circle cx="140" cy="50" r="5" fill="black"/>
  </svg>`
};

export const noseTypes = {
  straight: `<svg viewBox="0 0 200 150" xmlns="http://www.w3.org/2000/svg">
    <rect width="200" height="150" fill="white"/>
    <line x1="100" y1="30" x2="100" y2="100" stroke="black" stroke-width="2"/>
    <path d="M 85 100 Q 92 110 100 110 Q 108 110 115 100" fill="none" stroke="black" stroke-width="2"/>
  </svg>`,

  aquiline: `<svg viewBox="0 0 200 150" xmlns="http://www.w3.org/2000/svg">
    <rect width="200" height="150" fill="white"/>
    <path d="M 95 30 Q 95 60 105 80 L 105 100" fill="none" stroke="black" stroke-width="2"/>
    <path d="M 85 100 Q 92 110 100 110 Q 108 110 115 100" fill="none" stroke="black" stroke-width="2"/>
  </svg>`,

  button: `<svg viewBox="0 0 200 150" xmlns="http://www.w3.org/2000/svg">
    <rect width="200" height="150" fill="white"/>
    <line x1="100" y1="30" x2="100" y2="90" stroke="black" stroke-width="2"/>
    <circle cx="100" cy="100" r="12" fill="none" stroke="black" stroke-width="2"/>
  </svg>`,

  broad: `<svg viewBox="0 0 200 150" xmlns="http://www.w3.org/2000/svg">
    <rect width="200" height="150" fill="white"/>
    <line x1="100" y1="30" x2="100" y2="100" stroke="black" stroke-width="3"/>
    <path d="M 80 100 Q 90 115 100 115 Q 110 115 120 100" fill="none" stroke="black" stroke-width="2"/>
  </svg>`,

  narrow: `<svg viewBox="0 0 200 150" xmlns="http://www.w3.org/2000/svg">
    <rect width="200" height="150" fill="white"/>
    <line x1="100" y1="30" x2="100" y2="100" stroke="black" stroke-width="1.5"/>
    <path d="M 90 100 Q 95 108 100 108 Q 105 108 110 100" fill="none" stroke="black" stroke-width="2"/>
  </svg>`,

  roman: `<svg viewBox="0 0 200 150" xmlns="http://www.w3.org/2000/svg">
    <rect width="200" height="150" fill="white"/>
    <path d="M 98 30 Q 90 50 95 70 Q 98 85 100 100" fill="none" stroke="black" stroke-width="2"/>
    <path d="M 85 100 Q 92 110 100 110 Q 108 110 115 100" fill="none" stroke="black" stroke-width="2"/>
  </svg>`
};

export const mouthShapes = {
  full: `<svg viewBox="0 0 200 100" xmlns="http://www.w3.org/2000/svg">
    <rect width="200" height="100" fill="white"/>
    <path d="M 70 45 Q 100 35 130 45" fill="none" stroke="black" stroke-width="2.5"/>
    <path d="M 70 55 Q 100 65 130 55" fill="none" stroke="black" stroke-width="2.5"/>
  </svg>`,

  thin: `<svg viewBox="0 0 200 100" xmlns="http://www.w3.org/2000/svg">
    <rect width="200" height="100" fill="white"/>
    <line x1="70" y1="50" x2="130" y2="50" stroke="black" stroke-width="2"/>
  </svg>`,

  wide: `<svg viewBox="0 0 200 100" xmlns="http://www.w3.org/2000/svg">
    <rect width="200" height="100" fill="white"/>
    <path d="M 60 45 Q 100 35 140 45" fill="none" stroke="black" stroke-width="2.5"/>
    <path d="M 60 55 Q 100 65 140 55" fill="none" stroke="black" stroke-width="2.5"/>
  </svg>`,

  small: `<svg viewBox="0 0 200 100" xmlns="http://www.w3.org/2000/svg">
    <rect width="200" height="100" fill="white"/>
    <path d="M 85 45 Q 100 40 115 45" fill="none" stroke="black" stroke-width="2"/>
    <path d="M 85 55 Q 100 60 115 55" fill="none" stroke="black" stroke-width="2"/>
  </svg>`,

  bow: `<svg viewBox="0 0 200 100" xmlns="http://www.w3.org/2000/svg">
    <rect width="200" height="100" fill="white"/>
    <path d="M 70 45 Q 85 35 100 35 Q 115 35 130 45" fill="none" stroke="black" stroke-width="2"/>
    <path d="M 70 55 Q 100 65 130 55" fill="none" stroke="black" stroke-width="2"/>
  </svg>`,

  downturned: `<svg viewBox="0 0 200 100" xmlns="http://www.w3.org/2000/svg">
    <rect width="200" height="100" fill="white"/>
    <path d="M 70 45 Q 100 55 130 45" fill="none" stroke="black" stroke-width="2"/>
  </svg>`
};

export const eyebrowTypes = {
  straight: `<svg viewBox="0 0 200 80" xmlns="http://www.w3.org/2000/svg">
    <rect width="200" height="80" fill="white"/>
    <line x1="35" y1="40" x2="85" y2="40" stroke="black" stroke-width="3"/>
    <line x1="115" y1="40" x2="165" y2="40" stroke="black" stroke-width="3"/>
  </svg>`,

  arched: `<svg viewBox="0 0 200 80" xmlns="http://www.w3.org/2000/svg">
    <rect width="200" height="80" fill="white"/>
    <path d="M 35 45 Q 60 30 85 45" fill="none" stroke="black" stroke-width="3"/>
    <path d="M 115 45 Q 140 30 165 45" fill="none" stroke="black" stroke-width="3"/>
  </svg>`,

  rounded: `<svg viewBox="0 0 200 80" xmlns="http://www.w3.org/2000/svg">
    <rect width="200" height="80" fill="white"/>
    <path d="M 35 40 Q 60 35 85 40" fill="none" stroke="black" stroke-width="3"/>
    <path d="M 115 40 Q 140 35 165 40" fill="none" stroke="black" stroke-width="3"/>
  </svg>`,

  angled: `<svg viewBox="0 0 200 80" xmlns="http://www.w3.org/2000/svg">
    <rect width="200" height="80" fill="white"/>
    <path d="M 35 45 L 55 30 L 85 40" fill="none" stroke="black" stroke-width="3"/>
    <path d="M 115 40 L 145 30 L 165 45" fill="none" stroke="black" stroke-width="3"/>
  </svg>`,

  bushy: `<svg viewBox="0 0 200 80" xmlns="http://www.w3.org/2000/svg">
    <rect width="200" height="80" fill="white"/>
    <line x1="35" y1="40" x2="85" y2="40" stroke="black" stroke-width="5"/>
    <line x1="115" y1="40" x2="165" y2="40" stroke="black" stroke-width="5"/>
  </svg>`,

  thin: `<svg viewBox="0 0 200 80" xmlns="http://www.w3.org/2000/svg">
    <rect width="200" height="80" fill="white"/>
    <line x1="35" y1="40" x2="85" y2="40" stroke="black" stroke-width="1.5"/>
    <line x1="115" y1="40" x2="165" y2="40" stroke="black" stroke-width="1.5"/>
  </svg>`
};
