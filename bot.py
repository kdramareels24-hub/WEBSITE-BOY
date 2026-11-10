import os
import re
import io
import threading
from flask import Flask
import telebot

BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
bot = telebot.TeleBot(BOT_TOKEN)

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{BUSINESS_NAME}} | Global Enterprise Conglomerate</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  <style>
    .modal-active { display: flex !important; }
    .typing-cursor::after {
      content: '|';
      animation: blink 1s infinite;
    }
    @keyframes blink {
      0%, 100% { opacity: 1; }
      50% { opacity: 0; }
    }
    .video-bg {
      position: absolute;
      top: 50%;
      left: 50%;
      min-width: 100%;
      min-height: 100%;
      width: auto;
      height: auto;
      transform: translateX(-50%) translateY(-50%);
      object-fit: cover;
    }
  </style>
</head>
<body class="bg-slate-950 text-slate-100 font-sans antialiased selection:bg-cyan-500 selection:text-slate-950">

  <!-- TOP BAR -->
  <div class="bg-slate-950/95 text-slate-400 text-xs py-2.5 px-6 border-b border-slate-800/80 sticky top-0 z-50 backdrop-blur">
    <div class="max-w-7xl mx-auto flex justify-between items-center">
      <div class="flex items-center space-x-6">
        <span class="flex items-center"><i class="fa-solid fa-phone text-cyan-400 mr-2"></i>{{PHONE}}</span>
        <span class="hidden md:flex items-center"><i class="fa-solid fa-envelope text-cyan-400 mr-2"></i>{{EMAIL}}</span>
        <span class="hidden lg:flex items-center text-slate-500"><i class="fa-solid fa-shield-halved text-emerald-400 mr-2"></i>CIN/Govt Verified Legal Entity</span>
      </div>
      <div class="flex items-center space-x-4">
        <button onclick="openModal('loginModal')" class="text-slate-300 hover:text-cyan-400 transition font-semibold">Sign In</button>
        <span class="text-slate-700">|</span>
        <button onclick="openModal('registerModal')" class="bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold px-3 py-1 rounded text-xs transition">Client Portal</button>
      </div>
    </div>
  </div>

  <!-- NAVBAR -->
  <header class="bg-slate-900/80 backdrop-blur-xl border-b border-slate-800/80 sticky top-9 z-40">
    <div class="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
      <a href="#" class="flex items-center space-x-3 group">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-600 to-blue-500 flex items-center justify-center text-white font-black text-xl shadow-lg shadow-cyan-500/20 group-hover:scale-105 transition">
          <i class="fa-solid fa-chart-line"></i>
        </div>
        <div>
          <span class="text-lg md:text-2xl font-black tracking-tight text-white block leading-none">{{BUSINESS_NAME}}</span>
          <span class="text-[10px] tracking-widest uppercase text-cyan-400 font-bold">Group Holdings & Operations</span>
        </div>
      </a>

      <nav class="hidden xl:flex space-x-8 text-sm font-medium text-slate-300">
        <a href="#divisions" class="hover:text-cyan-400 transition">Operating Sectors</a>
        <a href="#operations" class="hover:text-cyan-400 transition">Infrastructure</a>
        <a href="#milestones" class="hover:text-cyan-400 transition">Timeline</a>
        <a href="#portfolio" class="hover:text-cyan-400 transition">Portfolio</a>
        <a href="#governance" class="hover:text-cyan-400 transition">Audit Desk</a>
        <a href="#contact" class="hover:text-cyan-400 transition">Contact</a>
      </nav>

      <div class="flex items-center space-x-3">
        <a href="#contact" class="hidden sm:inline-block border border-slate-700 hover:border-cyan-500/50 bg-slate-800/60 text-slate-200 hover:text-white px-4 py-2 rounded-lg text-xs font-bold uppercase tracking-wider transition">
          Procurement RFP
        </a>
      </div>
    </div>
  </header>

  <!-- HERO SECTION WITH LIVE WORKING VIDEO BACKGROUND -->
  <section class="relative min-h-[92vh] flex items-center justify-center overflow-hidden px-6">
    <!-- Live High-Reliability MP4 Video Stream -->
    <video autoplay loop muted playsinline class="video-bg z-0 opacity-40">
      <source src="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4" type="video/mp4">
    </video>

    <!-- Overlay Gradient Grids -->
    <div class="absolute inset-0 bg-gradient-to-b from-slate-950/80 via-slate-950/70 to-slate-950 z-10"></div>
    <div class="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(6,182,212,0.1)_0,transparent_70%)] z-10"></div>

    <div class="relative z-20 max-w-5xl mx-auto text-center py-24">
      <div class="inline-flex items-center gap-2.5 bg-slate-900/90 border border-cyan-500/40 px-4 py-1.5 rounded-full text-xs font-bold uppercase tracking-wider text-cyan-400 mb-8 backdrop-blur shadow-xl">
        <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
        <span>Active Operations & Verified Multi-Sector Enterprise</span>
      </div>

      <h1 class="text-4xl sm:text-6xl md:text-7xl font-black tracking-tight mb-6 leading-tight uppercase text-transparent bg-clip-text bg-gradient-to-r from-white via-slate-100 to-slate-400 drop-shadow-sm">
        {{BUSINESS_NAME}}
      </h1>

      <div class="text-xl sm:text-2xl md:text-3xl font-bold text-slate-300 mb-8 min-h-[44px]">
        <span class="text-cyan-400 font-normal">Specialized in: </span>
        <span id="dynamic-headline" class="typing-cursor text-white font-extrabold"></span>
      </div>

      <p class="text-sm md:text-lg text-slate-300/90 mb-10 max-w-3xl mx-auto leading-relaxed font-normal">
        An integrated commercial enterprise commanding high-scale operations across modern civil construction, nationwide logistics networks, technical software automation, and corporate wholesale procurement.
      </p>

      <div class="flex flex-wrap justify-center gap-4">
        <a href="#divisions" class="bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-black px-8 py-4 rounded-xl shadow-lg shadow-cyan-500/20 transition transform hover:-translate-y-0.5">
          <i class="fa-solid fa-layer-group mr-2"></i> Explore Operations
        </a>
        <a href="#governance" class="bg-slate-900/90 hover:bg-slate-800 border border-slate-700/80 px-8 py-4 rounded-xl font-bold transition backdrop-blur">
          <i class="fa-solid fa-building-circle-check mr-2 text-cyan-400"></i> Corporate Verification
        </a>
      </div>
    </div>
  </section>

  <!-- LIVE MARKET STATS & METRICS STRIP -->
  <div class="bg-slate-900 border-y border-slate-800/80 py-4 px-6 overflow-hidden">
    <div class="max-w-7xl mx-auto flex flex-wrap justify-between items-center gap-6 text-xs text-slate-400 font-mono">
      <div class="flex items-center space-x-2">
        <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
        <span class="text-white font-bold">OPERATIONAL SINCE:</span>
        <span class="text-cyan-400">{{YEAR}}</span>
      </div>
      <div class="flex items-center space-x-2">
        <span class="text-white font-bold">STATE REGISTRATION:</span>
        <span class="text-slate-300">ACTIVE & AUDITED</span>
      </div>
      <div class="flex items-center space-x-2">
        <span class="text-white font-bold">CONTRACT ACCREDITATION:</span>
        <span class="text-emerald-400">CLASS-A ENTERPRISE</span>
      </div>
      <div class="flex items-center space-x-2">
        <span class="text-white font-bold">SLA PERFORMANCE:</span>
        <span class="text-cyan-400">99.8% FULFILLMENT</span>
      </div>
    </div>
  </div>

  <!-- STATS MATRIX -->
  <section class="py-16 bg-slate-900/40 border-b border-slate-800/80">
    <div class="max-w-7xl mx-auto px-6 grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
      <div class="p-6 rounded-2xl bg-slate-900/60 border border-slate-800">
        <div class="text-3xl md:text-5xl font-black text-white mb-2">240+</div>
        <div class="text-xs uppercase font-bold text-cyan-400 tracking-wider">Executed Projects</div>
      </div>
      <div class="p-6 rounded-2xl bg-slate-900/60 border border-slate-800">
        <div class="text-3xl md:text-5xl font-black text-white mb-2">4</div>
        <div class="text-xs uppercase font-bold text-cyan-400 tracking-wider">Operating Sectors</div>
      </div>
      <div class="p-6 rounded-2xl bg-slate-900/60 border border-slate-800">
        <div class="text-3xl md:text-5xl font-black text-white mb-2">1,500+</div>
        <div class="text-xs uppercase font-bold text-cyan-400 tracking-wider">Institutional Partners</div>
      </div>
      <div class="p-6 rounded-2xl bg-slate-900/60 border border-slate-800">
        <div class="text-3xl md:text-5xl font-black text-white mb-2">100%</div>
        <div class="text-xs uppercase font-bold text-cyan-400 tracking-wider">Statutory Compliance</div>
      </div>
    </div>
  </section>

  <!-- OPERATING DIVISIONS (ALL-CATEGORY COVERAGE) -->
  <section id="divisions" class="py-28 max-w-7xl mx-auto px-6">
    <div class="text-center mb-20">
      <span class="text-cyan-400 font-extrabold tracking-widest text-xs uppercase">Core Verticals</span>
      <h2 class="text-3xl md:text-5xl font-black text-white mt-2">Diversified Industry Verticals</h2>
      <p class="text-slate-400 text-sm max-w-2xl mx-auto mt-4">Structured business divisions operating with independent capital, dedicated management, and unified corporate governance.</p>
      <div class="w-20 h-1 bg-gradient-to-r from-cyan-500 to-blue-500 mx-auto mt-4 rounded-full"></div>
    </div>

    <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
      <!-- 1. Civil & Infrastructure -->
      <div class="bg-slate-900/70 border border-slate-800 p-8 rounded-2xl hover:border-cyan-500/50 transition duration-300 group flex flex-col justify-between">
        <div>
          <div class="w-14 h-14 rounded-xl bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 flex items-center justify-center text-2xl mb-6 group-hover:scale-110 transition">
            <i class="fa-solid fa-city"></i>
          </div>
          <h3 class="text-xl font-bold text-white mb-3">Civil & Infrastructure</h3>
          <p class="text-slate-400 text-xs leading-relaxed mb-6">Commercial complexes, RCC structural developments, deep foundations, PEB warehouses, and municipal civil contracting.</p>
        </div>
        <div class="pt-4 border-t border-slate-800/80 text-[11px] font-mono text-cyan-400 uppercase">Division 01 // Heavy Civil</div>
      </div>

      <!-- 2. Logistics & Supply Chain -->
      <div class="bg-slate-900/70 border border-slate-800 p-8 rounded-2xl hover:border-cyan-500/50 transition duration-300 group flex flex-col justify-between">
        <div>
          <div class="w-14 h-14 rounded-xl bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 flex items-center justify-center text-2xl mb-6 group-hover:scale-110 transition">
            <i class="fa-solid fa-truck-fast"></i>
          </div>
          <h3 class="text-xl font-bold text-white mb-3">Freight & Logistics</h3>
          <p class="text-slate-400 text-xs leading-relaxed mb-6">Multi-modal freight mobility, temperature-controlled distribution, automated inventory docking, and nationwide freight supply.</p>
        </div>
        <div class="pt-4 border-t border-slate-800/80 text-[11px] font-mono text-cyan-400 uppercase">Division 02 // Mobility Network</div>
      </div>

      <!-- 3. Enterprise Digital & Software -->
      <div class="bg-slate-900/70 border border-slate-800 p-8 rounded-2xl hover:border-cyan-500/50 transition duration-300 group flex flex-col justify-between">
        <div>
          <div class="w-14 h-14 rounded-xl bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 flex items-center justify-center text-2xl mb-6 group-hover:scale-110 transition">
            <i class="fa-solid fa-server"></i>
          </div>
          <h3 class="text-xl font-bold text-white mb-3">Digital Systems & Cloud</h3>
          <p class="text-slate-400 text-xs leading-relaxed mb-6">Automated API routing architectures, distributed ERP databases, CRM pipelines, and corporate cloud communications.</p>
        </div>
        <div class="pt-4 border-t border-slate-800/80 text-[11px] font-mono text-cyan-400 uppercase">Division 03 // Tech & Cloud</div>
      </div>

      <!-- 4. General B2B Trade & Sourcing -->
      <div class="bg-slate-900/70 border border-slate-800 p-8 rounded-2xl hover:border-cyan-500/50 transition duration-300 group flex flex-col justify-between">
        <div>
          <div class="w-14 h-14 rounded-xl bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 flex items-center justify-center text-2xl mb-6 group-hover:scale-110 transition">
            <i class="fa-solid fa-boxes-packing"></i>
          </div>
          <h3 class="text-xl font-bold text-white mb-3">Wholesale & Trade</h3>
          <p class="text-slate-400 text-xs leading-relaxed mb-6">Direct factory raw materials, commercial inventory sourcing, corporate commodities distribution, and B2B supplier fulfillment.</p>
        </div>
        <div class="pt-4 border-t border-slate-800/80 text-[11px] font-mono text-cyan-400 uppercase">Division 04 // Global Sourcing</div>
      </div>
    </div>
  </section>

  <!-- INFRASTRUCTURE & FLEET DEEP DIVE -->
  <section id="operations" class="py-24 bg-slate-900/60 border-y border-slate-800/80">
    <div class="max-w-7xl mx-auto px-6">
      <div class="grid lg:grid-cols-2 gap-16 items-center">
        <div>
          <span class="text-cyan-400 font-extrabold tracking-widest text-xs uppercase">Operational Prowess</span>
          <h2 class="text-3xl md:text-5xl font-black text-white mt-2 mb-6">Industrial Capabilities & Physical Logistics</h2>
          <p class="text-slate-300 text-sm leading-relaxed mb-8">
            Operating with modern heavy machinery, cloud-synchronized dispatch units, and regional warehousing parks. Every vertical is managed under certified quality systems ensuring zero operational downtime.
          </p>

          <div class="grid grid-cols-2 gap-6 text-sm">
            <div class="border-l-2 border-cyan-500 pl-4">
              <h4 class="font-bold text-white text-base">Regional Hubs</h4>
              <p class="text-xs text-slate-400 mt-1">Multi-city fulfillment points handling heavy transit loads.</p>
            </div>
            <div class="border-l-2 border-cyan-500 pl-4">
              <h4 class="font-bold text-white text-base">Fleet Tracking</h4>
              <p class="text-xs text-slate-400 mt-1">Telematics-monitored distribution vehicles and equipment.</p>
            </div>
            <div class="border-l-2 border-cyan-500 pl-4">
              <h4 class="font-bold text-white text-base">Automated QA</h4>
              <p class="text-xs text-slate-400 mt-1">On-site structural, material, and electrical test labs.</p>
            </div>
            <div class="border-l-2 border-cyan-500 pl-4">
              <h4 class="font-bold text-white text-base">24/7 Dispatch</h4>
              <p class="text-xs text-slate-400 mt-1">Round-the-clock emergency support and procurement shifts.</p>
            </div>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <img src="https://images.unsplash.com/photo-1504307651254-35680f356dfd?q=80&w=600&auto=format&fit=crop" class="rounded-2xl border border-slate-800 h-64 w-full object-cover shadow-xl">
          <img src="https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?q=80&w=600&auto=format&fit=crop" class="rounded-2xl border border-slate-800 h-64 w-full object-cover shadow-xl mt-8">
        </div>
      </div>
    </div>
  </section>

  <!-- CORPORATE ROADMAP & TIMELINE -->
  <section id="milestones" class="py-28 max-w-7xl mx-auto px-6">
    <div class="text-center mb-20">
      <span class="text-cyan-400 font-extrabold tracking-widest text-xs uppercase">Progressive Growth</span>
      <h2 class="text-3xl md:text-5xl font-black text-white mt-2">Enterprise Journey & Trajectory</h2>
      <div class="w-20 h-1 bg-gradient-to-r from-cyan-500 to-blue-500 mx-auto mt-4 rounded-full"></div>
    </div>

    <div class="grid md:grid-cols-4 gap-8">
      <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl relative">
        <div class="text-2xl font-black text-cyan-400 mb-2">{{YEAR}}</div>
        <h4 class="font-bold text-white text-base mb-2">Corporate Foundation</h4>
        <p class="text-xs text-slate-400 leading-relaxed">Incorporated with formal state registrations, establishing initial commercial contracting footprint.</p>
      </div>

      <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl relative">
        <div class="text-2xl font-black text-cyan-400 mb-2">Expansion</div>
        <h4 class="font-bold text-white text-base mb-2">Multi-Sector Integration</h4>
        <p class="text-xs text-slate-400 leading-relaxed">Integrated freight management and wholesale procurement units into unified parent governance.</p>
      </div>

      <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl relative">
        <div class="text-2xl font-black text-cyan-400 mb-2">Modernization</div>
        <h4 class="font-bold text-white text-base mb-2">Digital Systems Deployment</h4>
        <p class="text-xs text-slate-400 leading-relaxed">Deployed real-time logistics tracking, automated client billing, and centralized audit reporting.</p>
      </div>

      <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl relative">
        <div class="text-2xl font-black text-cyan-400 mb-2">2026 Active</div>
        <h4 class="font-bold text-white text-base mb-2">Nationwide Scale</h4>
        <p class="text-xs text-slate-400 leading-relaxed">Managing multi-crore public & institutional contracts with certified Class-A compliance.</p>
      </div>
    </div>
  </section>

  <!-- UNIVERSAL PORTFOLIO SHOWCASE -->
  <section id="portfolio" class="py-24 bg-slate-900/40 border-y border-slate-800/80">
    <div class="max-w-7xl mx-auto px-6">
      <div class="text-center mb-16">
        <span class="text-cyan-400 font-extrabold tracking-widest text-xs uppercase">Track Record</span>
        <h2 class="text-3xl md:text-5xl font-black text-white mt-2">Executed Major Deployments</h2>
        <div class="w-20 h-1 bg-gradient-to-r from-cyan-500 to-blue-500 mx-auto mt-4 rounded-full"></div>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        <div class="group relative rounded-2xl overflow-hidden border border-slate-800">
          <img src="https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=600&auto=format&fit=crop" class="w-full h-72 object-cover group-hover:scale-105 transition duration-500">
          <div class="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/30 to-transparent flex flex-col justify-end p-6">
            <span class="text-cyan-400 text-[10px] font-mono uppercase font-bold">Civil Contracting</span>
            <h4 class="text-white font-bold text-lg">Commercial High-Rise Hub</h4>
          </div>
        </div>

        <div class="group relative rounded-2xl overflow-hidden border border-slate-800">
          <img src="https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?q=80&w=600&auto=format&fit=crop" class="w-full h-72 object-cover group-hover:scale-105 transition duration-500">
          <div class="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/30 to-transparent flex flex-col justify-end p-6">
            <span class="text-cyan-400 text-[10px] font-mono uppercase font-bold">Logistics & Supply</span>
            <h4 class="text-white font-bold text-lg">Distribution Center 04</h4>
          </div>
        </div>

        <div class="group relative rounded-2xl overflow-hidden border border-slate-800">
          <img src="https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=600&auto=format&fit=crop" class="w-full h-72 object-cover group-hover:scale-105 transition duration-500">
          <div class="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/30 to-transparent flex flex-col justify-end p-6">
            <span class="text-cyan-400 text-[10px] font-mono uppercase font-bold">Digital Systems</span>
            <h4 class="text-white font-bold text-lg">Multi-Tenant Cloud Datacenter</h4>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- GOVERNANCE & AUDIT CARD (FOR META VERIFICATION CRAWLERS) -->
  <section id="governance" class="py-28 max-w-7xl mx-auto px-6">
    <div class="grid lg:grid-cols-2 gap-16 items-center">
      <div>
        <span class="text-cyan-400 font-extrabold tracking-widest text-xs uppercase">Corporate Transparency</span>
        <h2 class="text-3xl md:text-5xl font-black text-white mt-2 mb-6">{{BUSINESS_NAME}}</h2>
        <p class="text-slate-300 text-sm leading-relaxed mb-6">
          Registered and operating under national corporate laws, <strong>{{BUSINESS_NAME}}</strong> maintains complete fiscal clarity, statutory filings, and direct vendor accountability.
        </p>
        <p class="text-slate-400 text-sm leading-relaxed mb-8">
          This portal functions as our verified public registry. All physical establishments, corporate offices, contact desks, and digital operations are cross-verified against official regulatory guidelines.
        </p>

        <div class="flex items-center space-x-6 text-xs text-slate-300">
          <div><i class="fa-solid fa-check-double text-cyan-400 mr-2"></i>Audited Tax Returns</div>
          <div><i class="fa-solid fa-check-double text-cyan-400 mr-2"></i>State Municipal Certs</div>
        </div>
      </div>

      <!-- AUDIT DATA BOX -->
      <div class="bg-slate-900 border border-slate-800 p-8 rounded-3xl shadow-2xl relative">
        <div class="flex items-center justify-between pb-6 mb-6 border-b border-slate-800">
          <div>
            <span class="text-[10px] text-cyan-400 font-mono uppercase font-bold tracking-widest">Registry File</span>
            <h4 class="text-lg font-bold text-white">Entity Credentials</h4>
          </div>
          <span class="bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 text-[10px] font-mono font-bold px-3 py-1 rounded-full uppercase">Verified Active</span>
        </div>

        <div class="space-y-5 text-sm">
          <div>
            <span class="text-xs text-slate-400 block font-mono uppercase">Full Legal Business Name</span>
            <span class="font-bold text-white text-base">{{BUSINESS_NAME}}</span>
          </div>
          <div>
            <span class="text-xs text-slate-400 block font-mono uppercase">Verified Corporate Communications</span>
            <a href="mailto:{{EMAIL}}" class="text-cyan-400 font-medium hover:underline">{{EMAIL}}</a>
          </div>
          <div>
            <span class="text-xs text-slate-400 block font-mono uppercase">Direct Commercial Phone</span>
            <a href="tel:{{PHONE}}" class="text-slate-200 font-medium hover:underline">{{PHONE}}</a>
          </div>
          <div>
            <span class="text-xs text-slate-400 block font-mono uppercase">Registered Headquarters</span>
            <span class="text-slate-300 leading-relaxed block">{{ADDRESS}}</span>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- COMPLIANCE & PRIVACY BYLAWS -->
  <section class="py-16 px-6 max-w-5xl mx-auto">
    <div class="bg-slate-900/60 border border-slate-800 p-8 rounded-2xl text-xs text-slate-400 space-y-4">
      <h3 class="text-sm font-bold text-white uppercase tracking-wider">Enterprise Compliance & Regulatory Terms</h3>
      <p>
        The operations of <strong>{{BUSINESS_NAME}}</strong> strictly abide by all regional trade commerce statutes. Communications, contact inquiries, client registrations, and tender RFPs received on this domain are archived strictly for commercial execution and corporate compliance.
      </p>
      <p>
        For verification of invoices, purchase orders, or formal statutory reviews, contact our administration desk at <strong>{{EMAIL}}</strong> or visit our head office at <strong>{{ADDRESS}}</strong>.
      </p>
    </div>
  </section>

  <!-- CONTACT & RFP FORM -->
  <section id="contact" class="py-24 bg-slate-900/80 border-t border-slate-800/80 px-6">
    <div class="max-w-7xl mx-auto grid lg:grid-cols-2 gap-16">
      <div>
        <span class="text-cyan-400 font-extrabold tracking-widest text-xs uppercase">Connect</span>
        <h2 class="text-3xl md:text-5xl font-black text-white mt-2 mb-6">Corporate Desk</h2>
        <p class="text-slate-400 text-sm mb-10 leading-relaxed">
          Submit procurement queries, vendor onboarding requests, or institutional tenders directly to our centralized desk.
        </p>

        <div class="space-y-6 text-sm">
          <div class="flex items-start space-x-4">
            <div class="w-12 h-12 rounded-xl bg-slate-800 border border-slate-700 flex items-center justify-center text-cyan-400 flex-shrink-0 mt-1">
              <i class="fa-solid fa-location-dot"></i>
            </div>
            <div>
              <span class="block text-slate-400 text-xs font-mono uppercase">Head Office</span>
              <span class="text-slate-200 font-medium">{{ADDRESS}}</span>
            </div>
          </div>

          <div class="flex items-start space-x-4">
            <div class="w-12 h-12 rounded-xl bg-slate-800 border border-slate-700 flex items-center justify-center text-cyan-400 flex-shrink-0 mt-1">
              <i class="fa-solid fa-envelope"></i>
            </div>
            <div>
              <span class="block text-slate-400 text-xs font-mono uppercase">Email Desk</span>
              <a href="mailto:{{EMAIL}}" class="text-cyan-400 font-medium hover:underline">{{EMAIL}}</a>
            </div>
          </div>

          <div class="flex items-start space-x-4">
            <div class="w-12 h-12 rounded-xl bg-slate-800 border border-slate-700 flex items-center justify-center text-cyan-400 flex-shrink-0 mt-1">
              <i class="fa-solid fa-phone"></i>
            </div>
            <div>
              <span class="block text-slate-400 text-xs font-mono uppercase">Telephone</span>
              <a href="tel:{{PHONE}}" class="text-slate-200 font-medium hover:underline">{{PHONE}}</a>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-slate-900 border border-slate-800 p-8 rounded-3xl shadow-xl">
        <h3 class="text-xl font-bold text-white mb-2">Request RFP / Commercial Quote</h3>
        <p class="text-xs text-slate-400 mb-6">Commercial responses dispatched within 24 working hours.</p>

        <form onsubmit="event.preventDefault(); alert('Commercial RFP recorded. Desk representative will contact you.');" class="space-y-4 text-sm">
          <div>
            <label class="block text-slate-400 text-xs mb-1 font-mono uppercase">Entity / Company Name</label>
            <input type="text" required class="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-cyan-400">
          </div>
          <div>
            <label class="block text-slate-400 text-xs mb-1 font-mono uppercase">Commercial Phone</label>
            <input type="tel" required class="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-cyan-400">
          </div>
          <div>
            <label class="block text-slate-400 text-xs mb-1 font-mono uppercase">Operating Vertical</label>
            <select class="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-cyan-400">
              <option>Civil Infrastructure & Engineering</option>
              <option>Logistics, Warehousing & Fleet</option>
              <option>Enterprise Digital & Cloud Systems</option>
              <option>Wholesale Procurement & Trade</option>
            </select>
          </div>
          <button type="submit" class="w-full bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-black py-4 rounded-xl transition shadow-lg shadow-cyan-500/20">
            Submit Commercial Inquiry
          </button>
        </form>
      </div>
    </div>
  </section>

  <!-- FOOTER -->
  <footer class="bg-slate-950 text-slate-500 text-xs py-12 border-t border-slate-800">
    <div class="max-w-7xl mx-auto px-6 grid md:grid-cols-4 gap-8 mb-10">
      <div>
        <span class="text-white font-bold text-base block mb-3">{{BUSINESS_NAME}}</span>
        <p class="text-slate-400 text-xs leading-relaxed">Integrated Commercial Conglomerate delivering multi-sector engineering, logistics, digital systems, and wholesale solutions.</p>
      </div>
      <div>
        <h5 class="text-white font-bold mb-3 uppercase tracking-wider text-[11px]">Divisions</h5>
        <ul class="space-y-2 text-slate-400">
          <li>Civil Infrastructure</li>
          <li>Logistics Networks</li>
          <li>Enterprise Cloud</li>
          <li>Commodity Trade</li>
        </ul>
      </div>
      <div>
        <h5 class="text-white font-bold mb-3 uppercase tracking-wider text-[11px]">Audit Links</h5>
        <ul class="space-y-2 text-slate-400">
          <li>Statutory Verification</li>
          <li>Quality Accreditations</li>
          <li>Privacy Policy</li>
          <li>Corporate Terms</li>
        </ul>
      </div>
      <div>
        <h5 class="text-white font-bold mb-3 uppercase tracking-wider text-[11px]">Corporate Office</h5>
        <p class="text-slate-400 leading-relaxed">{{ADDRESS}}</p>
      </div>
    </div>
    <div class="max-w-7xl mx-auto px-6 pt-8 border-t border-slate-900 flex flex-col md:flex-row justify-between items-center gap-4 text-[11px]">
      <p>© 2026 {{BUSINESS_NAME}}. All Rights Reserved.</p>
      <div class="flex space-x-6 text-slate-400">
        <span>Verified Entity</span>
        <span>•</span>
        <span>Encrypted SSL 256-Bit</span>
      </div>
    </div>
  </footer>

  <!-- SIGN IN MODAL WITH CONTINUE WITH GOOGLE -->
  <div id="loginModal" class="fixed inset-0 bg-black/80 backdrop-blur-md z-50 hidden items-center justify-center p-4">
    <div class="bg-slate-900 border border-slate-700/80 w-full max-w-md p-8 rounded-3xl shadow-2xl relative text-white">
      <button onclick="closeModal('loginModal')" class="absolute top-5 right-5 text-slate-400 hover:text-white text-xl">
        <i class="fa-solid fa-xmark"></i>
      </button>

      <h3 class="text-2xl font-black mb-1">Welcome Back</h3>
      <p class="text-xs text-slate-400 mb-6">Authenticate to access corporate contracts and invoice history</p>

      <!-- Google OAuth Button -->
      <button onclick="alert('Redirecting to Google Enterprise Identity Provider...');" class="w-full bg-white hover:bg-slate-100 text-slate-900 font-bold py-3 px-4 rounded-xl flex items-center justify-center space-x-3 mb-6 transition shadow">
        <svg class="w-5 h-5" viewBox="0 0 24 24">
          <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
          <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
          <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
          <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
        </svg>
        <span>Continue with Google</span>
      </button>

      <div class="flex items-center my-6">
        <div class="flex-grow border-t border-slate-800"></div>
        <span class="px-3 text-xs text-slate-500 uppercase font-mono">Or with email</span>
        <div class="flex-grow border-t border-slate-800"></div>
      </div>

      <form onsubmit="event.preventDefault(); alert('Authentication portal active. Access restricted to registered clients.');" class="space-y-4 text-sm">
        <div>
          <label class="block text-slate-400 text-xs mb-1">Corporate Email</label>
          <input type="email" required class="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-cyan-400">
        </div>
        <div>
          <label class="block text-slate-400 text-xs mb-1">Password</label>
          <input type="password" required class="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-cyan-400">
        </div>
        <button type="submit" class="w-full bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold py-3 rounded-xl transition">Sign In</button>
      </form>
    </div>
  </div>

  <!-- REGISTER MODAL WITH CONTINUE WITH GOOGLE -->
  <div id="registerModal" class="fixed inset-0 bg-black/80 backdrop-blur-md z-50 hidden items-center justify-center p-4">
    <div class="bg-slate-900 border border-slate-700/80 w-full max-w-md p-8 rounded-3xl shadow-2xl relative text-white">
      <button onclick="closeModal('registerModal')" class="absolute top-5 right-5 text-slate-400 hover:text-white text-xl">
        <i class="fa-solid fa-xmark"></i>
      </button>

      <h3 class="text-2xl font-black mb-1">Enterprise Registration</h3>
      <p class="text-xs text-slate-400 mb-6">Register your entity for direct corporate procurement accounts</p>

      <!-- Google OAuth Button -->
      <button onclick="alert('Redirecting to Google Enterprise Identity Provider...');" class="w-full bg-white hover:bg-slate-100 text-slate-900 font-bold py-3 px-4 rounded-xl flex items-center justify-center space-x-3 mb-6 transition shadow">
        <svg class="w-5 h-5" viewBox="0 0 24 24">
          <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
          <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
          <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
          <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
        </svg>
        <span>Sign up with Google</span>
      </button>

      <div class="flex items-center my-6">
        <div class="flex-grow border-t border-slate-800"></div>
        <span class="px-3 text-xs text-slate-500 uppercase font-mono">Or standard form</span>
        <div class="flex-grow border-t border-slate-800"></div>
      </div>

      <form onsubmit="event.preventDefault(); alert('Profile submitted for compliance screening.');" class="space-y-4 text-sm">
        <div>
          <label class="block text-slate-400 text-xs mb-1">Company / Entity Name</label>
          <input type="text" required class="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-cyan-400">
        </div>
        <div>
          <label class="block text-slate-400 text-xs mb-1">Corporate Email</label>
          <input type="email" required class="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-cyan-400">
        </div>
        <div>
          <label class="block text-slate-400 text-xs mb-1">Create Password</label>
          <input type="password" required class="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-cyan-400">
        </div>
        <button type="submit" class="w-full bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-black py-3 rounded-xl transition">
          Create Enterprise Account
        </button>
      </form>
    </div>
  </div>

  <script>
    function openModal(id) { document.getElementById(id).classList.add('modal-active'); }
    function closeModal(id) { document.getElementById(id).classList.remove('modal-active'); }

    const headlines = [
      "Commercial Infrastructure & Heavy Civil",
      "Nationwide Logistics & Supply Chain Fleet",
      "Distributed Cloud Software & Automation",
      "Institutional Commodity Procurement & B2B Trade"
    ];
    let hIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    const targetElement = document.getElementById("dynamic-headline");

    function typeEffect() {
      const currentText = headlines[hIndex];
      if (isDeleting) {
        targetElement.innerText = currentText.substring(0, charIndex - 1);
        charIndex--;
      } else {
        targetElement.innerText = currentText.substring(0, charIndex + 1);
        charIndex++;
      }

      let typingSpeed = isDeleting ? 35 : 75;

      if (!isDeleting && charIndex === currentText.length) {
        typingSpeed = 2000;
        isDeleting = true;
      } else if (isDeleting && charIndex === 0) {
        isDeleting = false;
        hIndex = (hIndex + 1) % headlines.length;
        typingSpeed = 400;
      }

      setTimeout(typeEffect, typingSpeed);
    }
    document.addEventListener("DOMContentLoaded", typeEffect);
  </script>
</body>
</html>
"""

def parse_details(text):
    data = {}
    lines = text.strip().split("\n")
    for line in lines:
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip().lower()
            val = val.strip()
            if "name" in key:
                data["name"] = val
            elif "email" in key or "gmail" in key:
                data["email"] = val
            elif "phone" in key or "mobile" in key or "number" in key:
                data["phone"] = val
            elif "address" in key or "location" in key:
                data["address"] = val
            elif "year" in key:
                data["year"] = val
    return data

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "🌐 *Universal Enterprise Conglomerate Website Generator*\n\n"
        "Ye bot ab full multi-page length wali cinematic live-video corporate website banayega jo kisi bhi category ke Meta BM ko bypass karegi.\n\n"
        "Format me bhejein:\n"
        "`Name: Pawan Private Enterprises`\n"
        "`Email: pawan@heoo.in`\n"
        "`Phone: +91 9876543210`\n"
        "`Address: Office No. 12, Commercial Tower, Sector 62, Noida 201301`\n"
        "`Year: 2018`\n"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    data = parse_details(message.text)
    
    if not all(k in data for k in ["name", "email", "phone", "address"]):
        bot.reply_to(
            message,
            "⚠️ *Format check karein:*\n"
            "`Name: Entity Name`\n"
            "`Email: your@heoo.in`\n"
            "`Phone: +919876543210`\n"
            "`Address: Full Address`\n"
            "`Year: 2019` *(Optional)*",
            parse_mode="Markdown"
        )
        return

    year = data.get("year", "2019")
    
    html_output = HTML_TEMPLATE
    html_output = html_output.replace("{{BUSINESS_NAME}}", data["name"])
    html_output = html_output.replace("{{EMAIL}}", data["email"])
    html_output = html_output.replace("{{PHONE}}", data["phone"])
    html_output = html_output.replace("{{ADDRESS}}", data["address"])
    html_output = html_output.replace("{{YEAR}}", year)

    clean_filename = re.sub(r'[^a-zA-Z0-9]', '_', data["name"]).lower() + "_index.html"
    file_bytes = io.BytesIO(html_output.encode("utf-8"))
    file_bytes.name = clean_filename

    caption = (
        f"🚀 *Full Enterprise Multi-Sector Website Ready!*\n\n"
        f"🏢 *Entity:* {data['name']}\n"
        f"📧 *Email:* {data['email']}\n"
        f"📞 *Phone:* {data['phone']}\n"
        f"📍 *Address:* {data['address']}\n\n"
        f"👉 Download karke Vercel par direct drop karein."
    )

    bot.send_document(
        chat_id=message.chat.id,
        document=file_bytes,
        caption=caption,
        parse_mode="Markdown"
    )

app = Flask(__name__)

@app.route('/')
def home():
    return "Universal Conglomerate Bot is running 24/7!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    threading.Thread(target=run_web, daemon=True).start()
    try:
        bot.remove_webhook()
    except Exception:
        pass
    print("Bot is starting polling...")
    bot.infinity_polling(timeout=20, long_polling_timeout=20)
