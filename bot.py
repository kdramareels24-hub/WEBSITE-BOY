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
  <title>{{BUSINESS_NAME}} | Corporate Enterprise & Multi-Industry Solutions</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
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
  </style>
</head>
<body class="bg-slate-50 text-slate-800 font-sans antialiased selection:bg-blue-600 selection:text-white">

  <!-- TOP BAR -->
  <div class="bg-slate-950 text-slate-300 text-xs py-2 px-6 border-b border-slate-800 hidden sm:block">
    <div class="max-w-7xl mx-auto flex justify-between items-center">
      <div class="flex items-center space-x-6">
        <span><i class="fa-solid fa-phone text-blue-500 mr-2"></i>{{PHONE}}</span>
        <span><i class="fa-solid fa-envelope text-blue-500 mr-2"></i>{{EMAIL}}</span>
      </div>
      <div class="flex items-center space-x-4">
        <span><i class="fa-solid fa-clock text-blue-500 mr-2"></i>Mon - Sat: 9:00 AM - 6:30 PM</span>
        <span class="text-slate-600">|</span>
        <button onclick="openModal('loginModal')" class="hover:text-blue-400 font-medium">Enterprise Portal</button>
      </div>
    </div>
  </div>

  <!-- NAVBAR -->
  <header class="bg-slate-900/90 backdrop-blur-md text-white sticky top-0 z-40 shadow-lg border-b border-slate-800">
    <div class="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
      <a href="#" class="flex items-center space-x-3">
        <div class="w-10 h-10 rounded-lg bg-blue-600 flex items-center justify-center text-white font-black text-xl shadow">
          <i class="fa-solid fa-cubes-stacked"></i>
        </div>
        <span class="text-xl md:text-2xl font-bold tracking-tight text-white">{{BUSINESS_NAME}}</span>
      </a>

      <nav class="hidden lg:flex space-x-7 text-sm font-medium">
        <a href="#divisions" class="hover:text-blue-400 transition">Operating Divisions</a>
        <a href="#infrastructure" class="hover:text-blue-400 transition">Capabilities</a>
        <a href="#portfolio" class="hover:text-blue-400 transition">Enterprise Portfolio</a>
        <a href="#governance" class="hover:text-blue-400 transition">Corporate Profile</a>
        <a href="#compliance" class="hover:text-blue-400 transition">Compliance</a>
        <a href="#contact" class="hover:text-blue-400 transition">Contact</a>
      </nav>

      <div class="flex items-center space-x-3">
        <button onclick="openModal('loginModal')" class="text-xs uppercase font-bold text-gray-300 hover:text-white px-3 py-2 border border-slate-700 rounded transition">
          Client Login
        </button>
        <button onclick="openModal('registerModal')" class="text-xs uppercase font-bold bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded transition shadow">
          Partner Access
        </button>
      </div>
    </div>
  </header>

  <!-- HERO SECTION WITH LIVE CORPORATE VIDEO -->
  <section class="relative min-h-[88vh] flex items-center justify-center bg-slate-950 text-white overflow-hidden px-6">
    <video autoplay loop muted playsinline class="absolute inset-0 w-full h-full object-cover opacity-25 z-0">
      <source src="https://assets.mixkit.co/videos/preview/mixkit-aerial-view-of-city-traffic-at-night-41546-large.mp4" type="video/mp4">
    </video>

    <div class="absolute inset-0 bg-gradient-to-b from-slate-950/85 via-slate-950/70 to-slate-950 z-10"></div>

    <div class="relative z-20 max-w-5xl mx-auto text-center py-20">
      <div class="inline-flex items-center gap-2 bg-blue-500/10 border border-blue-500/30 px-4 py-1.5 rounded-full text-xs font-bold uppercase tracking-wider text-blue-400 mb-6 backdrop-blur-sm">
        <span class="w-2.5 h-2.5 rounded-full bg-blue-400 animate-ping"></span>
        <span>Registered Enterprise Group & Multi-Sector Operations</span>
      </div>

      <h1 class="text-4xl sm:text-6xl md:text-7xl font-black tracking-tight mb-6 leading-tight uppercase">
        {{BUSINESS_NAME}}
      </h1>

      <div class="text-xl sm:text-2xl md:text-3xl font-semibold text-gray-200 mb-6 min-h-[40px]">
        <span class="text-blue-400">Integrated: </span>
        <span id="dynamic-headline" class="typing-cursor text-white font-bold">Commercial Infrastructure & Engineering</span>
      </div>

      <p class="text-sm md:text-lg text-gray-300 mb-10 max-w-3xl mx-auto leading-relaxed">
        Diversified corporate entity managing multi-disciplinary ventures across commercial contracting, supply chain networks, industrial asset logistics, and institutional procurement solutions.
      </p>

      <div class="flex flex-wrap justify-center gap-4">
        <a href="#contact" class="bg-blue-600 hover:bg-blue-700 text-white font-extrabold px-8 py-4 rounded-lg shadow-xl hover:shadow-blue-500/20 transition transform hover:-translate-y-0.5">
          <i class="fa-solid fa-briefcase mr-2"></i> Corporate Inquiries
        </a>
        <a href="#divisions" class="bg-slate-900/80 hover:bg-slate-800 border border-slate-700 px-8 py-4 rounded-lg font-bold transition backdrop-blur-sm">
          <i class="fa-solid fa-network-wired mr-2 text-blue-400"></i> Explore Divisions
        </a>
      </div>
    </div>
  </section>

  <!-- CORPORATE HIGHLIGHT STRIP -->
  <div class="bg-blue-600 py-4 px-6 text-white text-xs md:text-sm font-bold shadow-md">
    <div class="max-w-7xl mx-auto flex flex-wrap justify-around text-center gap-4">
      <span><i class="fa-solid fa-calendar-check mr-2"></i>Enterprise Incorporated: <strong>{{YEAR}}</strong></span>
      <span class="hidden md:inline">•</span>
      <span><i class="fa-solid fa-shield-halved mr-2"></i>Statutory & Corporate Compliant</span>
      <span class="hidden md:inline">•</span>
      <span><i class="fa-solid fa-file-contract mr-2"></i>Certified B2B Contracting Entity</span>
    </div>
  </div>

  <!-- STATS -->
  <section class="bg-white py-12 border-b border-gray-200">
    <div class="max-w-7xl mx-auto px-6 grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
      <div>
        <div class="text-3xl md:text-4xl font-extrabold text-slate-900">180+</div>
        <div class="text-xs uppercase font-semibold text-gray-500 mt-1">Enterprise Deliveries</div>
      </div>
      <div>
        <div class="text-3xl md:text-4xl font-extrabold text-slate-900">4</div>
        <div class="text-xs uppercase font-semibold text-gray-500 mt-1">Operational Divisions</div>
      </div>
      <div>
        <div class="text-3xl md:text-4xl font-extrabold text-slate-900">99.4%</div>
        <div class="text-xs uppercase font-semibold text-gray-500 mt-1">Service SLA Compliance</div>
      </div>
      <div>
        <div class="text-3xl md:text-4xl font-extrabold text-slate-900">100%</div>
        <div class="text-xs uppercase font-semibold text-gray-500 mt-1">Audit Alignment</div>
      </div>
    </div>
  </section>

  <!-- OPERATING DIVISIONS (4 IN 1 CATEGORIES) -->
  <section id="divisions" class="py-24 max-w-7xl mx-auto px-6">
    <div class="text-center mb-16">
      <span class="text-blue-600 font-bold tracking-wider text-xs uppercase">Core Divisions</span>
      <h2 class="text-3xl md:text-4xl font-black text-slate-900 mt-1">Multi-Disciplinary Business Operations</h2>
      <div class="w-16 h-1 bg-blue-600 mx-auto mt-3 rounded"></div>
    </div>

    <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
      <!-- 1. Civil & Infrastructure -->
      <div class="bg-white p-6 rounded-xl border border-gray-200 shadow hover:shadow-lg transition">
        <div class="w-12 h-12 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center text-xl mb-4">
          <i class="fa-solid fa-building"></i>
        </div>
        <h3 class="text-lg font-bold text-slate-900 mb-2">Civil & Construction</h3>
        <p class="text-gray-600 text-xs leading-relaxed">Turnkey commercial construction, foundational engineering, and civil facility development.</p>
      </div>

      <!-- 2. Logistics & Supply Chain -->
      <div class="bg-white p-6 rounded-xl border border-gray-200 shadow hover:shadow-lg transition">
        <div class="w-12 h-12 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center text-xl mb-4">
          <i class="fa-solid fa-truck-ramp-box"></i>
        </div>
        <h3 class="text-lg font-bold text-slate-900 mb-2">Logistics & Supply Chain</h3>
        <p class="text-gray-600 text-xs leading-relaxed">Fleet management, regional freight warehousing, distribution hubs, and last-mile logistics.</p>
      </div>

      <!-- 3. Enterprise Tech & Solutions -->
      <div class="bg-white p-6 rounded-xl border border-gray-200 shadow hover:shadow-lg transition">
        <div class="w-12 h-12 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center text-xl mb-4">
          <i class="fa-solid fa-microchip"></i>
        </div>
        <h3 class="text-lg font-bold text-slate-900 mb-2">Enterprise Digital</h3>
        <p class="text-gray-600 text-xs leading-relaxed">ERP architectures, automated communication channels, cloud integrations, and corporate workflows.</p>
      </div>

      <!-- 4. General B2B Procurement -->
      <div class="bg-white p-6 rounded-xl border border-gray-200 shadow hover:shadow-lg transition">
        <div class="w-12 h-12 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center text-xl mb-4">
          <i class="fa-solid fa-handshake"></i>
        </div>
        <h3 class="text-lg font-bold text-slate-900 mb-2">B2B Trade & Sourcing</h3>
        <p class="text-gray-600 text-xs leading-relaxed">Bulk raw material procurement, institutional wholesale supply, and corporate vendor contracting.</p>
      </div>
    </div>
  </section>

  <!-- INFRASTRUCTURE CAPABILITIES -->
  <section id="infrastructure" class="bg-slate-900 text-white py-20 px-6">
    <div class="max-w-7xl mx-auto">
      <div class="text-center mb-16">
        <span class="text-blue-400 font-bold tracking-wider text-xs uppercase">Operational Scope</span>
        <h2 class="text-3xl md:text-4xl font-black mt-1">Enterprise Asset Infrastructure</h2>
        <div class="w-16 h-1 bg-blue-500 mx-auto mt-3 rounded"></div>
      </div>

      <div class="grid md:grid-cols-3 gap-8">
        <div class="bg-slate-800 p-8 rounded-xl border border-slate-700">
          <i class="fa-solid fa-warehouse text-3xl text-blue-400 mb-4"></i>
          <h4 class="font-bold text-lg mb-2">Centralized Facilities</h4>
          <p class="text-xs text-gray-400 leading-relaxed">Modern regional hubs designed for inventory management, equipment staging, and corporate operational dispatch.</p>
        </div>
        <div class="bg-slate-800 p-8 rounded-xl border border-slate-700">
          <i class="fa-solid fa-shield-virus text-3xl text-blue-400 mb-4"></i>
          <h4 class="font-bold text-lg mb-2">Regulatory Auditing</h4>
          <p class="text-xs text-gray-400 leading-relaxed">Internal auditing teams maintaining compliance with state tax registrations, commercial bylaws, and occupational safety codes.</p>
        </div>
        <div class="bg-slate-800 p-8 rounded-xl border border-slate-700">
          <i class="fa-solid fa-chart-line text-3xl text-blue-400 mb-4"></i>
          <h4 class="font-bold text-lg mb-2">Scale & Capital Capacity</h4>
          <p class="text-xs text-gray-400 leading-relaxed">Robust credit framework enabling execution of large institutional work orders without logistical bottlenecks.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- UNIVERSAL PORTFOLIO -->
  <section id="portfolio" class="py-24 max-w-7xl mx-auto px-6">
    <div class="text-center mb-16">
      <span class="text-blue-600 font-bold tracking-wider text-xs uppercase">Key Executions</span>
      <h2 class="text-3xl md:text-4xl font-black text-slate-900 mt-1">Integrated Corporate Portfolio</h2>
      <div class="w-16 h-1 bg-blue-600 mx-auto mt-3 rounded"></div>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
      <div class="relative group rounded-xl overflow-hidden shadow">
        <img src="https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=600&auto=format&fit=crop" class="w-full h-64 object-cover group-hover:scale-105 transition duration-500">
        <div class="absolute inset-0 bg-gradient-to-t from-slate-950/90 via-slate-950/20 to-transparent flex flex-col justify-end p-6">
          <span class="text-blue-400 text-xs font-bold uppercase">Commercial Project</span>
          <h4 class="text-white font-bold text-lg">Corporate Headquarters Development</h4>
        </div>
      </div>
      <div class="relative group rounded-xl overflow-hidden shadow">
        <img src="https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?q=80&w=600&auto=format&fit=crop" class="w-full h-64 object-cover group-hover:scale-105 transition duration-500">
        <div class="absolute inset-0 bg-gradient-to-t from-slate-950/90 via-slate-950/20 to-transparent flex flex-col justify-end p-6">
          <span class="text-blue-400 text-xs font-bold uppercase">Supply Chain Hub</span>
          <h4 class="text-white font-bold text-lg">Automated Logistics Facility</h4>
        </div>
      </div>
      <div class="relative group rounded-xl overflow-hidden shadow">
        <img src="https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=600&auto=format&fit=crop" class="w-full h-64 object-cover group-hover:scale-105 transition duration-500">
        <div class="absolute inset-0 bg-gradient-to-t from-slate-950/90 via-slate-950/20 to-transparent flex flex-col justify-end p-6">
          <span class="text-blue-400 text-xs font-bold uppercase">Digital Architecture</span>
          <h4 class="text-white font-bold text-lg">Enterprise Cloud Infrastructure</h4>
        </div>
      </div>
    </div>
  </section>

  <!-- GOVERNANCE & BUSINESS DATA -->
  <section id="governance" class="bg-gray-100 py-24 px-6 border-y border-gray-200">
    <div class="max-w-7xl mx-auto grid md:grid-cols-2 gap-12 items-center">
      <div>
        <span class="text-blue-600 font-bold tracking-wider text-xs uppercase">Corporate Governance</span>
        <h2 class="text-3xl md:text-4xl font-black text-slate-900 mt-1 mb-6">{{BUSINESS_NAME}}</h2>
        <p class="text-gray-600 text-sm leading-relaxed mb-4">
          Established in <strong>{{YEAR}}</strong>, <strong>{{BUSINESS_NAME}}</strong> functions as an integrated commercial establishment managing diversified industrial and corporate operations. 
        </p>
        <p class="text-gray-600 text-sm leading-relaxed mb-6">
          Our centralized management framework ensures all regional undertakings adhere strictly to statutory tax compliance, municipal standards, and transparent client engagement protocols.
        </p>
      </div>

      <!-- AUDIT CARD -->
      <div class="bg-white p-8 rounded-xl border border-gray-200 shadow-md">
        <h3 class="text-lg font-bold text-slate-900 mb-6 pb-2 border-b border-gray-200 flex items-center">
          <i class="fa-solid fa-certificate text-blue-600 mr-2.5"></i> Legal Entity Verification Data
        </h3>
        <div class="space-y-4 text-sm">
          <div>
            <span class="text-xs uppercase font-bold text-gray-400 block">Registered Entity Name</span>
            <span class="font-bold text-slate-900">{{BUSINESS_NAME}}</span>
          </div>
          <div>
            <span class="text-xs uppercase font-bold text-gray-400 block">Corporate Communications</span>
            <a href="mailto:{{EMAIL}}" class="font-medium text-blue-600 hover:underline">{{EMAIL}}</a>
          </div>
          <div>
            <span class="text-xs uppercase font-bold text-gray-400 block">Verified Commercial Desk</span>
            <a href="tel:{{PHONE}}" class="font-medium text-slate-800 hover:underline">{{PHONE}}</a>
          </div>
          <div>
            <span class="text-xs uppercase font-bold text-gray-400 block">Registered Operational Office</span>
            <span class="text-gray-700 leading-relaxed">{{ADDRESS}}</span>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- COMPLIANCE & PRIVACY -->
  <section id="compliance" class="py-16 px-6 max-w-5xl mx-auto">
    <div class="bg-white p-8 rounded-xl border border-gray-200 shadow-sm text-xs text-gray-500 space-y-4">
      <h3 class="text-sm font-bold text-slate-900 uppercase tracking-wide">Enterprise Privacy & Operational Bylaws</h3>
      <p>
        This portal is operated by <strong>{{BUSINESS_NAME}}</strong>. All communications, inquiries, transactions, and corporate correspondence submitted through this domain are strictly processed for commercial contract fulfillment, vendor onboarding, and corporate auditing.
      </p>
      <p>
        For official audits, tax compliance invoices, or corporate inquiries, write directly to <strong>{{EMAIL}}</strong> or visit our registered facilities at <strong>{{ADDRESS}}</strong>.
      </p>
    </div>
  </section>

  <!-- CONTACT -->
  <section id="contact" class="bg-slate-900 text-white py-24 px-6">
    <div class="max-w-7xl mx-auto grid md:grid-cols-2 gap-12">
      <div>
        <span class="text-blue-400 font-bold uppercase tracking-wider text-xs">Direct Desk</span>
        <h2 class="text-3xl md:text-4xl font-black mb-6">Contact Corporate Office</h2>
        <p class="text-gray-400 text-sm mb-8">
          Inquiries regarding enterprise procurement, multi-divisional contracts, or regulatory verification.
        </p>

        <div class="space-y-6 text-sm">
          <div class="flex items-start space-x-4">
            <div class="w-10 h-10 rounded bg-slate-800 flex items-center justify-center text-blue-400 flex-shrink-0 mt-1">
              <i class="fa-solid fa-location-dot"></i>
            </div>
            <div>
              <span class="block text-gray-400 text-xs font-semibold uppercase">Office Address</span>
              <span class="text-gray-200 font-medium leading-relaxed">{{ADDRESS}}</span>
            </div>
          </div>

          <div class="flex items-start space-x-4">
            <div class="w-10 h-10 rounded bg-slate-800 flex items-center justify-center text-blue-400 flex-shrink-0 mt-1">
              <i class="fa-solid fa-envelope"></i>
            </div>
            <div>
              <span class="block text-gray-400 text-xs font-semibold uppercase">Official Email</span>
              <a href="mailto:{{EMAIL}}" class="text-blue-400 hover:underline">{{EMAIL}}</a>
            </div>
          </div>

          <div class="flex items-start space-x-4">
            <div class="w-10 h-10 rounded bg-slate-800 flex items-center justify-center text-blue-400 flex-shrink-0 mt-1">
              <i class="fa-solid fa-phone"></i>
            </div>
            <div>
              <span class="block text-gray-400 text-xs font-semibold uppercase">Direct Telephone</span>
              <a href="tel:{{PHONE}}" class="text-gray-200 hover:underline">{{PHONE}}</a>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-slate-800 p-8 rounded-xl border border-slate-700 shadow-xl">
        <h3 class="text-xl font-bold mb-4">General Enterprise Inquiry</h3>
        <form onsubmit="event.preventDefault(); alert('Inquiry recorded. Representative will respond within 24 hours.');" class="space-y-4 text-sm">
          <div>
            <label class="block text-gray-300 mb-1 text-xs">Entity / Client Name</label>
            <input type="text" required class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2.5 text-white focus:outline-none focus:border-blue-400">
          </div>
          <div>
            <label class="block text-gray-300 mb-1 text-xs">Contact Number</label>
            <input type="tel" required class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2.5 text-white focus:outline-none focus:border-blue-400">
          </div>
          <div>
            <label class="block text-gray-300 mb-1 text-xs">Operating Division</label>
            <select class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2.5 text-white focus:outline-none focus:border-blue-400">
              <option>Civil Infrastructure & Engineering</option>
              <option>Supply Chain & Logistics</option>
              <option>Enterprise Digital Solutions</option>
              <option>General Wholesale & B2B Trade</option>
            </select>
          </div>
          <button type="submit" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded transition shadow">Submit Commercial Request</button>
        </form>
      </div>
    </div>
  </section>

  <!-- FOOTER -->
  <footer class="bg-slate-950 text-gray-500 text-xs py-8 text-center border-t border-slate-800">
    <div class="max-w-7xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-4">
      <p>© 2026 {{BUSINESS_NAME}}. All Rights Reserved.</p>
      <div class="flex space-x-6 text-gray-400">
        <a href="#compliance" class="hover:underline">Privacy Policy</a>
        <a href="#compliance" class="hover:underline">Terms of Service</a>
        <a href="#contact" class="hover:underline">Governance Desk</a>
      </div>
    </div>
  </footer>

  <!-- MODALS -->
  <div id="loginModal" class="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 hidden items-center justify-center p-4">
    <div class="bg-slate-900 border border-slate-700 w-full max-w-md p-6 rounded-xl shadow-2xl relative text-white">
      <button onclick="closeModal('loginModal')" class="absolute top-4 right-4 text-gray-400 hover:text-white text-xl">
        <i class="fa-solid fa-xmark"></i>
      </button>
      <h3 class="text-xl font-bold mb-1">Enterprise Client Login</h3>
      <p class="text-xs text-gray-400 mb-6">Access your procurement contracts, invoices, and service milestones</p>
      <form onsubmit="event.preventDefault(); alert('Authentication portal active. Access restricted to registered clients.');" class="space-y-4 text-sm">
        <div>
          <label class="block text-gray-400 text-xs mb-1">Corporate Email</label>
          <input type="email" required class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-white focus:outline-none focus:border-blue-500">
        </div>
        <div>
          <label class="block text-gray-400 text-xs mb-1">Password</label>
          <input type="password" required class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-white focus:outline-none focus:border-blue-500">
        </div>
        <button type="submit" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2.5 rounded transition">Authenticate</button>
      </form>
    </div>
  </div>

  <div id="registerModal" class="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 hidden items-center justify-center p-4">
    <div class="bg-slate-900 border border-slate-700 w-full max-w-md p-6 rounded-xl shadow-2xl relative text-white">
      <button onclick="closeModal('registerModal')" class="absolute top-4 right-4 text-gray-400 hover:text-white text-xl">
        <i class="fa-solid fa-xmark"></i>
      </button>
      <h3 class="text-xl font-bold mb-1">Partner Onboarding</h3>
      <p class="text-xs text-gray-400 mb-6">Register your company to initiate B2B trade partnerships</p>
      <form onsubmit="event.preventDefault(); alert('Registration recorded. Profile activation will be dispatched to your corporate email.');" class="space-y-4 text-sm">
        <div>
          <label class="block text-gray-400 text-xs mb-1">Legal Company Name</label>
          <input type="text" required class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-white focus:outline-none focus:border-blue-500">
        </div>
        <div>
          <label class="block text-gray-400 text-xs mb-1">Official Email</label>
          <input type="email" required class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-white focus:outline-none focus:border-blue-500">
        </div>
        <div>
          <label class="block text-gray-400 text-xs mb-1">Create Password</label>
          <input type="password" required class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-white focus:outline-none focus:border-blue-500">
        </div>
        <button type="submit" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2.5 rounded transition">Register Enterprise Account</button>
      </form>
    </div>
  </div>

  <script>
    function openModal(id) { document.getElementById(id).classList.add('modal-active'); }
    function closeModal(id) { document.getElementById(id).classList.remove('modal-active'); }

    const headlines = [
      "Commercial Infrastructure & Engineering",
      "Integrated Supply Chain & Regional Logistics",
      "Enterprise Digital Systems & Automation",
      "Institutional Wholesale & Procurement Solutions"
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

      let typingSpeed = isDeleting ? 40 : 80;

      if (!isDeleting && charIndex === currentText.length) {
        typingSpeed = 2200;
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
        "🏢 *Multi-Sector Corporate Enterprise Website Generator*\n\n"
        "Ye bot ek Universal Corporate Conglomerate website generate karega jo kisi bhi business category (Trading, Tech, Construction, Logistics) ke Meta Verification ko approve karwa sakti hai.\n\n"
        "Format me details bhejo:\n"
        "`Name: Apex Global Enterprises`\n"
        "`Email: contact@heoo.in`\n"
        "`Phone: +91 9876543210`\n"
        "`Address: Office 401, Business Center, Sector 18, Noida 201301`\n"
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
            "`Email: contact@heoo.in`\n"
            "`Phone: +919876543210`\n"
            "`Address: Registered Address`\n"
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
        f"🌐 *Universal Enterprise HTML Ready!*\n\n"
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
    return "Universal Enterprise Bot is running 24/7!"

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
