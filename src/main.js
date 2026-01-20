import './style.css'
import './fonts.css'

// ============================================
// TYPING ANIMATION
// ============================================
const typingSequence = [
  { action: 'type', text: 'Perpetual Learner', delay: 80 },
  { action: 'pause', duration: 1500 },
  { action: 'delete', count: 17, delay: 40 },
  { action: 'pause', duration: 300 },
  { action: 'type', text: 'Engineer', delay: 80 },
  { action: 'pause', duration: 800 },
  { action: 'move-start', delay: 60 },
  { action: 'type', text: 'Embedded Systems ', delay: 70 },
  { action: 'move-end', delay: 60 },
  { action: 'pause', duration: 600 },
  { action: 'type', text: ' & Robotics Enthusiast', delay: 70 },
  { action: 'pause', duration: 3000 }
];

class TypeWriter {
  constructor(element) {
    this.el = element;
    this.text = '';
    this.cursorPos = 0;
    this.sequenceIndex = 0;
  }

  async run() {
    while (this.sequenceIndex < typingSequence.length) {
      const step = typingSequence[this.sequenceIndex];

      switch (step.action) {
        case 'type':
          for (const char of step.text) {
            this.text = this.text.slice(0, this.cursorPos) + char + this.text.slice(this.cursorPos);
            this.cursorPos++;
            this.render();
            await this.sleep(step.delay);
          }
          break;
        case 'delete':
          for (let i = 0; i < step.count; i++) {
            if (this.cursorPos > 0) {
              this.text = this.text.slice(0, this.cursorPos - 1) + this.text.slice(this.cursorPos);
              this.cursorPos--;
              this.render();
              await this.sleep(step.delay);
            }
          }
          break;
        case 'move-start':
          while (this.cursorPos > 0) {
            this.cursorPos--;
            this.render();
            await this.sleep(step.delay);
          }
          break;
        case 'move-end':
          while (this.cursorPos < this.text.length) {
            this.cursorPos++;
            this.render();
            await this.sleep(step.delay);
          }
          break;
        case 'pause':
          await this.sleep(step.duration);
          break;
      }

      this.sequenceIndex++;
    }
    this.el.innerHTML = `<span class="text-cyber-green">>_</span> <span class="text-white/80">${this.text}</span>`;
  }

  render() {
    const before = this.text.slice(0, this.cursorPos);
    const after = this.text.slice(this.cursorPos);
    this.el.innerHTML = `<span class="text-cyber-green">>_</span> <span class="text-white/80">${before}<span class="typing-cursor">|</span>${after}</span>`;
  }

  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// ============================================
// DATA
// ============================================

const aboutContent = `
<p><span class="text-cyber-green">$</span> I'm an <span class="text-cyber-cyan">Embedded Software Engineer</span> at <a href="https://accoladeelectronics.com" class="text-cyber-amber hover:underline" target="_blank">Accolade Electronics Pvt. Ltd.</a></p>
<p><span class="text-cyber-green">$</span> I work on <span class="text-cyber-amber">Software Defined Vehicles (SDVs)</span>, telematics systems, Qt Applications, and network modules. My role involves developing embedded software that's shaping the future of automotive technology.</p>
<p><span class="text-cyber-green">$</span> I've got a bunch of interests, maybe not too many. At the core I am interested in <span class="text-cyber-cyan">Robotics</span>, <span class="text-cyber-amber">deep learning</span>, and <span class="text-cyber-green">embedded systems</span>. But I'm also drawn to computer networks, electronics, machine vision, NLP, mathematics, hardware drivers and more. There's just so much fascinating stuff out there!</p>
<p><span class="text-cyber-green">$</span> B.Tech in Electrical and Electronics Engineering from <a href="https://vnit.ac.in/" class="text-cyber-cyan hover:underline" target="_blank">VNIT Nagpur</a>.</p>
<p class="text-cyber-cyan animate-pulse">█</p>
`;

const experience = [
  {
    company: "Accolade Electronics Pvt. Ltd. (R&D)",
    position: "Software Engineer",
    duration: "Jun 2023 – Present",
    location: "Pune, India",
    subsections: [
      {
        title: "Embedded Systems Development",
        bullets: [
          "Reduced sleep current of Samsung eMMC from 52.1mA to 0.11mA through low-level driver modifications; verified with 15 TBW burn-in testing.",
          "Created minimal task scheduler (RTOS) for Renesas RH850 MCU handling context switching and multitasking.",
          "Performed complete board bring-up for Renesas RH850 U2A8 including peripheral init, clock config, and HAL development.",
          "Implemented DoIP (Diagnostics over IP) on LWIP TCP/IP stack for TCU Ethernet variant, enabling remote diagnostics.",
          "Built Embedded Linux using Buildroot for RISC-V, configured and emulated on QEMU."
        ]
      },
      {
        title: "Telematics Control Unit (TCU)",
        bullets: [
          "Enhanced network module of Advanced TCU 4G as part of Product Improvement team.",
          "Developed Ethernet Bridge middleware for seamless protocol translation between CAN and Ethernet stacks.",
          "Hardened FOTA pipeline with CRC-validated headers and fail-safe metadata, preventing bricked field units.",
          "Integrated Edge Agent into Deep Data Logger project for cloud communication."
        ]
      },
      {
        title: "Tools and Automation",
        bullets: [
          "Developed proprietary CAN-based ECU Service Tool for secure UDS firmware updates.",
          "Upgraded service tool for TCU 4G/2G devices, enabling recovery of 400+ field units.",
          "Automated device validation with Qt-based utility, reducing processing time by 30%."
        ]
      }
    ]
  },
  {
    company: "IIT Guwahati (IITG)",
    position: "Research Assistant",
    duration: "Jun 2022 – Nov 2022",
    location: "Guwahati, India",
    description: [
      "Researched coreset selection strategies (greedy, k-center) for efficient data sampling in ML pipelines.",
      "Evaluated gradient approximation quality on SVHN, CIFAR-10/100 with reduced training overhead.",
      "Built modular training pipeline with custom AlexNet, optimizers, LR schedulers, and visualization tools."
    ]
  },
  {
    company: "IvLabs, VNIT",
    position: "Undergraduate Researcher & Vice Chairman",
    duration: "Jun 2020 – May 2023",
    location: "Nagpur, India",
    description: [
      "Developed face-recognition door unlock system achieving 81.4% accuracy on LFW using FaceNet/ArcFace.",
      "Implemented U-Net and YOLO pipelines for image segmentation on PASCAL VOC 2012.",
      "Applied PID controllers and Hermite curves for TurtleBot navigation in ROS.",
      "Supervised 40+ lab members, conducting workshops on programming, CV, and embedded systems."
    ]
  }
];

const blogPosts = [
  {
    title: "ARM Cortex-M Hardfault Handling",
    excerpt: "Debugging hardfaults on Cortex-M, covering stack frames, HFSR/CFSR registers, and exception entry.",
    date: "Aug 19, 2025",
    tags: ["ARM", "Cortex-M", "Debugging", "C"],
    link: "https://abd-01.github.io/posts/2025-08-19-ARM-Cortex-M/"
  },
  {
    title: "QEMU Essentials",
    excerpt: "System emulation basics for ARM/RISC-V environments, networking, and host-guest communication.",
    date: "Jul 15, 2025",
    tags: ["QEMU", "Linux", "Virtualization"],
    link: "https://abd-01.github.io/posts/2025-07-15-QEMU/"
  },
  {
    title: "Memory Arenas",
    excerpt: "Manual memory management for bare-metal systems. Arena allocators in C.",
    date: "Jun 25, 2025",
    tags: ["C", "Memory", "Allocators"],
    link: "https://abd-01.github.io/posts/2025-06-25-Arenas/"
  },
  {
    title: "Getting to Know Lambdas in C++",
    excerpt: "Closures, captures, and functional power of lambda expressions in modern C++.",
    date: "May 11, 2025",
    tags: ["C++", "Lambdas", "Modern C++"],
    link: "https://abd-01.github.io/posts/2025-05-11-Lambdas-in-CPP/"
  },
  {
    title: "Learning C++ via Advent of Code 2024 [Day 9]",
    excerpt: "Solving the disk fragmenting challenge from AoC 2024 with optimized C++ algorithms.",
    date: "Dec 30, 2024",
    tags: ["C++", "AoC", "Algorithms"],
    link: "https://abd-01.github.io/posts/2025-01-05-AOC-Day-9/"
  },
  {
    title: "Hello World!",
    excerpt: "Hi, I have made new version of my website. If you are seeing this, it is live.",
    date: "Aug 12, 2024",
    tags: ["sphinx", "vite", "github pages", "blog"],
    link: "https://abd-01.github.io/posts/2024-08-12-hello-world/"
  }
];

const projectsData = [
  {
    id: '01',
    title: 'ESP32 Crash Diagnostics in QEMU',
    category: 'EMBEDDED',
    description: 'ESP32 crash diagnostics workflow on QEMU with ESP-IDF, FreeRTOS fault injection, coredump capture & CRC validation.',
    tags: ['QEMU', 'ESP-IDF', 'FreeRTOS', 'Flask'],
    link: 'https://abd-01.github.io/esp32-guru-upload/coredump/'
  },
  {
    id: '02',
    title: 'Connected Vehicle Server Protocol',
    category: 'IOT',
    description: 'Flask-based MQTT server for protobuf-encoded telemetry with real-time Socket.IO updates and CLI interface.',
    tags: ['Flask', 'Protobuf', 'MQTT', 'Socket.IO'],
    link: 'https://abd-01.github.io/Flask-Protobuf/'
  },
  {
    id: '03',
    title: 'Open-Set Multi-Source Multi-Target Domain Adaptation',
    category: 'AI_RESEARCH',
    description: 'NeurIPS\'21 paper on unsupervised domain adaptation using prototypical networks, LOF pseudo-labeling, and GNN attention.',
    tags: ['PyTorch', 'GNN', 'NeurIPS'],
    link: 'https://ivlabs.github.io/os-nsmt/'
  },
  {
    id: '04',
    title: 'Face Unlock',
    category: 'COMPUTER_VISION',
    description: 'Triplet Network and FaceNet implementation with ResNet backbone for one-shot face recognition door lock system.',
    tags: ['PyTorch', 'OpenCV', 'FaceNet'],
    link: 'https://bit.ly/unlockface'
  },
  {
    id: '05',
    title: 'Object Detection',
    category: 'COMPUTER_VISION',
    description: 'Sliding window technique with two-stage detector enhanced with OverFeat framework on Raccoon Dataset.',
    tags: ['Python', 'TensorFlow', 'OverFeat'],
    link: 'https://github.com/IvLabs/Object-Detection'
  },
  {
    id: '06',
    title: 'Autonomous Turtle Chase',
    category: 'ROBOTICS',
    description: 'PID control with Kåsa circle fitting for trajectory deduction and autonomous interception in ROS Turtlesim.',
    tags: ['ROS', 'PID', 'C++', 'Python'],
    link: 'https://abd-01.github.io/reports/flytbase/'
  }
];

const miniProjectsData = [
  {
    title: 'Flappy Ball',
    description: 'SDL2/C++ game engine implementation cross-compiled for WebAssembly (Emscripten) and Android.',
    tags: ['C++', 'SDL2', 'WASM', 'Android'],
    link: 'https://abd-01.github.io/SDL2-Flappy-Ball/'
  },
  {
    title: 'Bezier curves',
    description: 'Interactive visualization of cubic Bezier curves and spline interpolation using raw canvas and geometry math.',
    tags: ['Javascript', 'Math', 'Geometry'],
    link: 'https://github.com/Muhammed-Abdullah-Shaikh/bezier'
  }
];

const skills = {
  "Embedded Systems": ["RH850", "ARM Cortex-M", "QEMU", "Buildroot", "u-boot", "FreeRTOS", "RISC-V", "Bare-metal", "Driver Dev", "Embedded Linux", "RTOS", "BSP Bring-up", "HAL", "NXP", "Renesas", "TI", "STM32", "ESP32", "ESP-IDF"],
  "Communication Protocols": ["CAN", "UDS", "DoIP", "Ethernet", "UART", "I2C", "MQTT", "Protobuf"],
  "Programming Languages": ["Embedded C", "C", "C++", "Python", "Java", "MATLAB", "LabVIEW"],
  "Machine Learning": ["PyTorch", "TensorFlow", "Model Optimization", "Face Recognition", "Object Detection", "Edge AI"],
  "Software Tools": ["Git", "CMake", "Qt", "LaTeX", "Vim", "Docker", "Sphinx", "Android Studio"],
  "Robotics": ["ROS2/ROS", "Gazebo", "RaspberryPi", "Path Planning", "PID Control", "Kobuki TurtleBot 2"]
};

// ============================================
// RENDER FUNCTIONS
// ============================================

function renderAbout() {
  const container = document.querySelector('#about-content');
  if (container) container.innerHTML = aboutContent;
}

function renderExperience() {
  const container = document.querySelector('#experience-timeline');
  if (!container) return;

  container.innerHTML = experience.map(exp => `
    <div class="relative pl-8 border-l border-cyber-cyan/30 mb-8 last:mb-0">
      <div class="absolute -left-[5px] top-0 w-2 h-2 bg-cyber-cyan shadow-[0_0_8px_#00FFF0]"></div>
      <div class="flex flex-col md:flex-row md:items-center justify-between mb-2">
        <h3 class="text-xl font-bold uppercase">${exp.company}</h3>
        <span class="font-mono text-[10px] text-white/40 uppercase">${exp.duration}</span>
      </div>
      <p class="text-cyber-cyan font-mono text-xs mb-4 uppercase tracking-tighter">${exp.position}</p>
      <div class="space-y-4">
        ${exp.subsections ? exp.subsections.map(sub => `
          <div>
            <h4 class="text-[10px] font-mono text-white/30 uppercase mb-2">// ${sub.title}</h4>
            <ul class="space-y-1.5 list-none">
              ${sub.bullets.map(b => `
                <li class="flex items-start text-xs text-white/60 leading-relaxed font-sans">
                  <span class="text-cyber-cyan mr-2 mt-1.5 w-1 h-1 bg-cyber-cyan flex-shrink-0"></span>
                  ${b}
                </li>
              `).join('')}
            </ul>
          </div>
        `).join('') : exp.description ? `
          <ul class="space-y-1.5 list-none">
            ${exp.description.map(b => `
              <li class="flex items-start text-xs text-white/60 leading-relaxed font-sans">
                <span class="text-cyber-cyan mr-2 mt-1.5 w-1 h-1 bg-cyber-cyan flex-shrink-0"></span>
                ${b}
              </li>
            `).join('')}
          </ul>
        ` : ''}
      </div>
    </div>
  `).join('');
}

function renderBlog() {
  const container = document.querySelector('#blog-grid');
  if (!container) return;

  container.innerHTML = blogPosts.map(post => `
    <a href="${post.link}" target="_blank" class="group block bg-industrial-gray/20 border border-white/5 p-6 hover:border-cyber-amber/50 transition-all cursor-pointer">
      <div class="flex justify-between items-center mb-3">
        <span class="font-mono text-[9px] text-cyber-amber uppercase tracking-widest">Log</span>
        <span class="font-mono text-[9px] text-white/50">${post.date}</span>
      </div>
      <h3 class="text-base font-bold mb-2 group-hover:text-cyber-amber transition-colors uppercase leading-tight">${post.title}</h3>
      <p class="text-white/40 text-xs mb-4 leading-relaxed line-clamp-2 italic">${post.excerpt}</p>
      <div class="flex flex-wrap gap-2">
        ${post.tags.map(t => `<span class="px-1.5 py-0.5 border border-cyber-amber/30 text-cyber-amber/60 text-[9px] uppercase font-mono">${t}</span>`).join('')}
      </div>
    </a>
  `).join('');
}

function renderProjects() {
  const container = document.querySelector('#project-grid');
  if (!container) return;

  container.innerHTML = projectsData.map(p => `
    <a href="${p.link}" target="_blank" class="group block relative bg-cyber-black border border-white/5 p-6 hover:border-cyber-cyan/30 transition-all hover:bg-cyber-cyan/5 cursor-pointer">
      <div class="font-mono text-[9px] mb-2 text-cyber-cyan/40">ID_${p.id} // ${p.category}</div>
      <h3 class="text-base font-bold mb-2 group-hover:text-cyber-cyan transition-colors uppercase tracking-tighter">${p.title}</h3>
      <p class="text-white/30 text-xs mb-4 leading-relaxed">${p.description}</p>
      <div class="flex flex-wrap gap-1.5">
        ${p.tags.map(t => `<span class="px-1.5 py-0.5 border border-cyber-cyan/30 text-cyber-cyan/60 text-[9px] uppercase font-mono">${t}</span>`).join('')}
      </div>
    </a>
  `).join('');
}

function renderMiniProjects() {
  const container = document.querySelector('#mini-project-grid');
  if (!container) return;

  container.innerHTML = miniProjectsData.map(p => `
    <a href="${p.link}" target="_blank" class="group block relative bg-cyber-black border border-white/5 p-6 hover:border-cyber-amber/30 transition-all hover:bg-cyber-amber/5 cursor-pointer">
      <div class="font-mono text-[9px] mb-3 text-cyber-amber/40">// SUB_MODULE</div>
      <h3 class="text-base font-bold mb-2 group-hover:text-cyber-amber transition-colors uppercase tracking-tight">${p.title}</h3>
      <p class="text-white/40 text-[11px] mb-4 leading-relaxed">${p.description}</p>
      <div class="flex flex-wrap gap-1.5">
        ${p.tags.map(t => `<span class="px-1.5 py-0.5 border border-cyber-amber/30 text-cyber-amber/60 text-[9px] uppercase font-mono">${t}</span>`).join('')}
      </div>
    </a>
  `).join('');
}

function renderSkills() {
  const container = document.querySelector('#skills-grid');
  if (!container) return;

  container.innerHTML = Object.entries(skills).map(([cat, list]) => `
    <div class="p-6 bg-white/[0.01] border border-white/5">
      <h4 class="font-mono text-[10px] uppercase text-cyber-cyan/60 mb-4 tracking-widest">// ${cat}</h4>
      <div class="flex flex-wrap gap-2">
        ${list.map(s => `
          <span class="px-2 py-1 bg-white/5 border border-cyber-cyan/30 text-white/50 text-[10px] font-mono">
            ${s}
          </span>
        `).join('')}
      </div>
    </div>
  `).join('');
}

// ============================================
// CONTACT FORM
// ============================================
function initContact() {
  const form = document.querySelector('#ContactForm');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = document.querySelector('#submitButton');
    const originalText = btn.textContent;
    btn.textContent = 'TRANSMITTING...';
    btn.disabled = true;

    try {
      const decode = (s) => atob(s);
      const whToken = decode('UzJabm1KSlBoNjl4TXQ4eE5ZbkNpdi1MVlBwZHdSWnpFYWVrc1J5Zmg2ZzRUUEpRYnZvXzR0NWxRYWthMk1IWHdYMl8=');
      const whId = decode('MTQxNzgyMTMxNTgwODc1OTgzOA==');
      const d = decode('ZGlzY29yZC5jb20vYXBpL3dlYmhvb2tz');

      const payload = {
        content: '<@701479951479865384>, Transmission from Portfolio!',
        embeds: [{
          title: `Message from ${form.name.value}`,
          description: `**Source**: ${form.email.value}\n**Data**: ${form.message.value}`,
          color: 0x00FFF0
        }]
      };

      await fetch(`https://${d}/${whId}/${whToken}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      btn.textContent = 'TRANSMISSION_ACK';
      form.reset();
    } catch (err) {
      btn.textContent = 'LINK_FAILURE';
    } finally {
      setTimeout(() => {
        btn.textContent = originalText;
        btn.disabled = false;
      }, 3000);
    }
  });
}

// ============================================
// INIT
// ============================================
document.addEventListener('DOMContentLoaded', () => {
  renderAbout();
  renderExperience();
  renderBlog();
  renderProjects();
  renderMiniProjects();
  renderSkills();
  initContact();

  // Typing animation
  const typingEl = document.querySelector('#typing-role');
  if (typingEl) {
    const typewriter = new TypeWriter(typingEl);
    typewriter.run();
  }

  // Mobile Menu
  const navBtn = document.querySelector('#mobile-menu-btn');
  const navMenu = document.querySelector('#mobile-menu');
  if (navBtn && navMenu) {
    navBtn.addEventListener('click', () => {
      navMenu.classList.toggle('hidden');
      navMenu.classList.toggle('flex');
    });
    navMenu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
      navMenu.classList.add('hidden');
      navMenu.classList.remove('flex');
    }));
  }
});
