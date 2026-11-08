import os
import re
import io
import telebot

# YAHAN APNA TELEGRAM BOT TOKEN DAALO (BotFather se lekar)
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
bot = telebot.TeleBot(BOT_TOKEN)

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{BUSINESS_NAME}} | Civil Engineering & Construction</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    .modal-active { display: flex !important; }
  </style>
</head>
<body class="bg-gray-50 text-slate-800 font-sans antialiased">

  <!-- TOP BAR -->
  <div class="bg-slate-950 text-gray-300 text-xs py-2 px-6 border-b border-slate-800 hidden sm:block">
    <div class="max-w-7xl mx-auto flex justify-between items-center">
      <div class="flex items-center space-x-6">
        <span><i class="fa-solid fa-phone text-amber-500 mr-2"></i>{{PHONE}}</span>
        <span><i class="fa-solid fa-envelope text-amber-500 mr-2"></i>{{EMAIL}}</span>
      </div>
      <div class="flex items-center space-x-4">
        <span><i class="fa-solid fa-clock text-amber-500 mr-2"></i>Mon - Sat: 9:00 AM - 7:00 PM</span>
        <span class="text-slate-600">|</span>
        <button onclick="openModal('loginModal')" class="hover:text-amber-400 font-medium">Client Login</button>
      </div>
    </div>
  </div>

  <!-- NAVBAR -->
  <header class="bg-slate-900 text-white sticky top-0 z-40 shadow-lg border-b border-slate-800">
    <div class="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
      <a href="#" class="flex items-center space-x-3">
        <div class="w-10 h-10 rounded-lg bg-amber-500 flex items-center justify-center text-slate-950 font-black text-xl shadow">
          <i class="fa-solid fa-building-wheat"></i>
        </div>
        <span class="text-xl md:text-2xl font-bold tracking-tight text-white">{{BUSINESS_NAME}}</span>
      </a>

      <nav class="hidden lg:flex space-x-7 text-sm font-medium">
        <a href="#services" class="hover:text-amber-400 transition">Services</a>
        <a href="#machinery" class="hover:text-amber-400 transition">Machinery</a>
        <a href="#projects" class="hover:text-amber-400 transition">Portfolio</a>
        <a href="#about" class="hover:text-amber-400 transition">About Entity</a>
        <a href="#compliance" class="hover:text-amber-400 transition">Compliance</a>
        <a href="#contact" class="hover:text-amber-400 transition">Contact</a>
      </nav>

      <div class="flex items-center space-x-3">
        <button onclick="openModal('loginModal')" class="text-xs uppercase font-bold text-gray-300 hover:text-white px-3 py-2 border border-slate-700 rounded transition">
          Sign In
        </button>
        <button onclick="openModal('registerModal')" class="text-xs uppercase font-bold bg-amber-500 hover:bg-amber-600 text-slate-950 px-4 py-2 rounded transition shadow">
          Register
        </button>
      </div>
    </div>
  </header>

  <!-- HERO SECTION -->
  <section class="relative bg-slate-950 text-white py-32 px-6 overflow-hidden">
    <div class="absolute inset-0 z-0">
      <img src="https://images.unsplash.com/photo-1541888946425-d0fbb1861593?q=80&w=1600&auto=format&fit=crop" class="w-full h-full object-cover opacity-20">
    </div>
    <div class="relative z-10 max-w-4xl mx-auto text-center">
      <span class="inline-block bg-amber-500/20 text-amber-400 border border-amber-500/30 px-4 py-1.5 rounded-full text-xs font-bold uppercase tracking-wider mb-6">
        Licensed Infrastructure & Civil Contracting Firm
      </span>
      <h1 class="text-4xl md:text-6xl font-black tracking-tight mb-6 leading-tight">
        {{BUSINESS_NAME}}
      </h1>
      <p class="text-lg md:text-xl text-gray-300 mb-10 max-w-3xl mx-auto leading-relaxed">
        Specializing in commercial structures, residential complexes, deep foundation excavation, and turnkey industrial installations across the region.
      </p>
      <div class="flex flex-wrap justify-center gap-4">
        <a href="#contact" class="bg-amber-500 hover:bg-amber-600 text-slate-950 font-bold px-8 py-3.5 rounded shadow-lg transition">Get Quotation</a>
        <a href="#projects" class="bg-slate-800/80 hover:bg-slate-800 border border-slate-700 px-8 py-3.5 rounded font-semibold transition">Our Work</a>
      </div>
    </div>
  </section>

  <!-- CREDENTIALS STRIP -->
  <div class="bg-amber-500 py-4 px-6 text-slate-950 text-xs md:text-sm font-bold shadow-md">
    <div class="max-w-7xl mx-auto flex flex-wrap justify-around text-center gap-4">
      <span><i class="fa-solid fa-calendar-check mr-2"></i>Active Operations Since: <strong>{{YEAR}}</strong></span>
      <span class="hidden md:inline">•</span>
      <span><i class="fa-solid fa-shield-halved mr-2"></i>Registered Civil Contractor</span>
      <span class="hidden md:inline">•</span>
      <span><i class="fa-solid fa-file-invoice mr-2"></i>Tax & Regulatory Compliant Entity</span>
    </div>
  </div>

  <!-- STATS COUNTER -->
  <section class="bg-white py-12 border-b border-gray-200">
    <div class="max-w-7xl mx-auto px-6 grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
      <div>
        <div class="text-3xl md:text-4xl font-extrabold text-slate-900">120+</div>
        <div class="text-xs uppercase font-semibold text-gray-500 mt-1">Completed Sites</div>
      </div>
      <div>
        <div class="text-3xl md:text-4xl font-extrabold text-slate-900">45+</div>
        <div class="text-xs uppercase font-semibold text-gray-500 mt-1">Heavy Machinery Units</div>
      </div>
      <div>
        <div class="text-3xl md:text-4xl font-extrabold text-slate-900">300+</div>
        <div class="text-xs uppercase font-semibold text-gray-500 mt-1">Certified Technicians</div>
      </div>
      <div>
        <div class="text-3xl md:text-4xl font-extrabold text-slate-900">100%</div>
        <div class="text-xs uppercase font-semibold text-gray-500 mt-1">Safety Compliant</div>
      </div>
    </div>
  </section>

  <!-- SERVICES SECTION -->
  <section id="services" class="py-24 max-w-7xl mx-auto px-6">
    <div class="text-center mb-16">
      <span class="text-amber-600 font-bold tracking-wider text-xs uppercase">What We Build</span>
      <h2 class="text-3xl md:text-4xl font-black text-slate-900 mt-1">Core Construction Verticals</h2>
      <div class="w-16 h-1 bg-amber-500 mx-auto mt-3 rounded"></div>
    </div>

    <div class="grid md:grid-cols-3 gap-8">
      <div class="bg-white rounded-xl overflow-hidden border border-gray-200 shadow hover:shadow-lg transition">
        <img src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?q=80&w=600&auto=format&fit=crop" class="h-52 w-full object-cover">
        <div class="p-6">
          <h3 class="text-xl font-bold text-slate-900 mb-2">Residential Real Estate</h3>
          <p class="text-gray-600 text-sm leading-relaxed mb-4">Complete turnkey construction of residential villas, multi-family housing complexes, and high-rise apartments.</p>
          <span class="text-xs font-semibold text-amber-600 uppercase">RCC & Seismic Isolation</span>
        </div>
      </div>

      <div class="bg-white rounded-xl overflow-hidden border border-gray-200 shadow hover:shadow-lg transition">
        <img src="https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=600&auto=format&fit=crop" class="h-52 w-full object-cover">
        <div class="p-6">
          <h3 class="text-xl font-bold text-slate-900 mb-2">Commercial Hubs & Offices</h3>
          <p class="text-gray-600 text-sm leading-relaxed mb-4">Corporate headquarters, retail shopping complexes, showrooms, and mixed-use civil developments.</p>
          <span class="text-xs font-semibold text-amber-600 uppercase">Structural Steel & Curtain Walls</span>
        </div>
      </div>

      <div class="bg-white rounded-xl overflow-hidden border border-gray-200 shadow hover:shadow-lg transition">
        <img src="https://images.unsplash.com/photo-1503387762-592deb58ef4e?q=80&w=600&auto=format&fit=crop" class="h-52 w-full object-cover">
        <div class="p-6">
          <h3 class="text-xl font-bold text-slate-900 mb-2">Industrial Warehouses</h3>
          <p class="text-gray-600 text-sm leading-relaxed mb-4">Logistics parks, factory sheds, cold storage facilities, and high-strength industrial flooring systems.</p>
          <span class="text-xs font-semibold text-amber-600 uppercase">PEB & Heavy Foundations</span>
        </div>
      </div>
    </div>
  </section>

  <!-- MACHINERY FLEET & CAPACITY -->
  <section id="machinery" class="bg-slate-900 text-white py-20 px-6">
    <div class="max-w-7xl mx-auto">
      <div class="text-center mb-16">
        <span class="text-amber-400 font-bold tracking-wider text-xs uppercase">Machinery & Logistics</span>
        <h2 class="text-3xl md:text-4xl font-black mt-1">Our Heavy Fleet Capabilities</h2>
        <div class="w-16 h-1 bg-amber-500 mx-auto mt-3 rounded"></div>
      </div>

      <div class="grid md:grid-cols-4 gap-6">
        <div class="bg-slate-800 p-6 rounded-lg border border-slate-700">
          <i class="fa-solid fa-truck-monster text-3xl text-amber-400 mb-4"></i>
          <h4 class="font-bold text-lg mb-2">Excavation Fleet</h4>
          <p class="text-xs text-gray-400">Tracked excavators, backhoes, and trenchers for bulk site leveling.</p>
        </div>
        <div class="bg-slate-800 p-6 rounded-lg border border-slate-700">
          <i class="fa-solid fa-truck-droplet text-3xl text-amber-400 mb-4"></i>
          <h4 class="font-bold text-lg mb-2">Concrete Mixers</h4>
          <p class="text-xs text-gray-400">Transit mixers and mobile batching plants providing high-grade ready-mix concrete.</p>
        </div>
        <div class="bg-slate-800 p-6 rounded-lg border border-slate-700">
          <i class="fa-solid fa-arrow-up-from-ground-water text-3xl text-amber-400 mb-4"></i>
          <h4 class="font-bold text-lg mb-2">Tower Cranes</h4>
          <p class="text-xs text-gray-400">Self-erecting and fixed tower cranes for multi-story lifting operations.</p>
        </div>
        <div class="bg-slate-800 p-6 rounded-lg border border-slate-700">
          <i class="fa-solid fa-compass-drafting text-3xl text-amber-400 mb-4"></i>
          <h4 class="font-bold text-lg mb-2">Quality Labs</h4>
          <p class="text-xs text-gray-400">On-site compaction, soil testing, and concrete cube crushing equipment.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- EXTENDED PORTFOLIO -->
  <section id="projects" class="py-24 max-w-7xl mx-auto px-6">
    <div class="text-center mb-16">
      <span class="text-amber-600 font-bold tracking-wider text-xs uppercase">Track Record</span>
      <h2 class="text-3xl md:text-4xl font-black text-slate-900 mt-1">Executed Engineering Projects</h2>
      <div class="w-16 h-1 bg-amber-500 mx-auto mt-3 rounded"></div>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
      <div class="relative group rounded-xl overflow-hidden shadow">
        <img src="https://images.unsplash.com/photo-1590381105924-c72589b9ef3f?q=80&w=600&auto=format&fit=crop" class="w-full h-64 object-cover group-hover:scale-105 transition duration-500">
        <div class="absolute inset-0 bg-gradient-to-t from-slate-950/90 via-slate-950/20 to-transparent flex flex-col justify-end p-6">
          <span class="text-amber-400 text-xs font-bold uppercase">Civil Infrastructure</span>
          <h4 class="text-white font-bold text-lg">Deep Foundation Excavation</h4>
        </div>
      </div>
      <div class="relative group rounded-xl overflow-hidden shadow">
        <img src="https://images.unsplash.com/photo-1541971875076-8f970d573be6?q=80&w=600&auto=format&fit=crop" class="w-full h-64 object-cover group-hover:scale-105 transition duration-500">
        <div class="absolute inset-0 bg-gradient-to-t from-slate-950/90 via-slate-950/20 to-transparent flex flex-col justify-end p-6">
          <span class="text-amber-400 text-xs font-bold uppercase">Commercial Complex</span>
          <h4 class="text-white font-bold text-lg">Multi-Tier Steel Framework</h4>
        </div>
      </div>
      <div class="relative group rounded-xl overflow-hidden shadow">
        <img src="https://images.unsplash.com/photo-1504307651254-35680f356dfd?q=80&w=600&auto=format&fit=crop" class="w-full h-64 object-cover group-hover:scale-105 transition duration-500">
        <div class="absolute inset-0 bg-gradient-to-t from-slate-950/90 via-slate-950/20 to-transparent flex flex-col justify-end p-6">
          <span class="text-amber-400 text-xs font-bold uppercase">Site Supervision</span>
          <h4 class="text-white font-bold text-lg">Architectural Quality Control</h4>
        </div>
      </div>
      <div class="relative group rounded-xl overflow-hidden shadow">
        <img src="https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?q=80&w=600&auto=format&fit=crop" class="w-full h-64 object-cover group-hover:scale-105 transition duration-500">
        <div class="absolute inset-0 bg-gradient-to-t from-slate-950/90 via-slate-950/20 to-transparent flex flex-col justify-end p-6">
          <span class="text-amber-400 text-xs font-bold uppercase">Commercial Hub</span>
          <h4 class="text-white font-bold text-lg">Corporate Interior Redesign</h4>
        </div>
      </div>
      <div class="relative group rounded-xl overflow-hidden shadow">
        <img src="https://images.unsplash.com/photo-1581094794329-c8112a89af12?q=80&w=600&auto=format&fit=crop" class="w-full h-64 object-cover group-hover:scale-105 transition duration-500">
        <div class="absolute inset-0 bg-gradient-to-t from-slate-950/90 via-slate-950/20 to-transparent flex flex-col justify-end p-6">
          <span class="text-amber-400 text-xs font-bold uppercase">Industrial Facility</span>
          <h4 class="text-white font-bold text-lg">Heavy Structural Decking</h4>
        </div>
      </div>
      <div class="relative group rounded-xl overflow-hidden shadow">
        <img src="https://images.unsplash.com/photo-1531834685032-c34bf0d84c77?q=80&w=600&auto=format&fit=crop" class="w-full h-64 object-cover group-hover:scale-105 transition duration-500">
        <div class="absolute inset-0 bg-gradient-to-t from-slate-950/90 via-slate-950/20 to-transparent flex flex-col justify-end p-6">
          <span class="text-amber-400 text-xs font-bold uppercase">Urban Logistics</span>
          <h4 class="text-white font-bold text-lg">Automated Warehouse Shed</h4>
        </div>
      </div>
    </div>
  </section>

  <!-- ABOUT & CORPORATE PROFILE -->
  <section id="about" class="bg-gray-100 py-24 px-6 border-y border-gray-200">
    <div class="max-w-7xl mx-auto grid md:grid-cols-2 gap-12 items-center">
      <div>
        <span class="text-amber-600 font-bold tracking-wider text-xs uppercase">Corporate Profile</span>
        <h2 class="text-3xl md:text-4xl font-black text-slate-900 mt-1 mb-6">{{BUSINESS_NAME}}</h2>
        <p class="text-gray-600 text-sm leading-relaxed mb-4">
          Established in <strong>{{YEAR}}</strong>, <strong>{{BUSINESS_NAME}}</strong> has grown into an autonomous engineering and commercial contracting organization. We manage heavy-civil earthworks, commercial RCC construction, residential projects, and infrastructure contracting.
        </p>
        <p class="text-gray-600 text-sm leading-relaxed mb-6">
          Every project complies with municipal bylaws, national safety codes, and rigorous audit standards, maintaining complete alignment with regional tax, labor, and corporate guidelines.
        </p>
      </div>

      <!-- AUDIT CARD -->
      <div class="bg-white p-8 rounded-xl border border-gray-200 shadow-md">
        <h3 class="text-lg font-bold text-slate-900 mb-6 pb-2 border-b border-gray-200 flex items-center">
          <i class="fa-solid fa-building-circle-check text-amber-500 mr-2.5"></i> Verification & Business Data
        </h3>
        <div class="space-y-4 text-sm">
          <div>
            <span class="text-xs uppercase font-bold text-gray-400 block">Legal Entity Name</span>
            <span class="font-bold text-slate-900">{{BUSINESS_NAME}}</span>
          </div>
          <div>
            <span class="text-xs uppercase font-bold text-gray-400 block">Official Business Email</span>
            <a href="mailto:{{EMAIL}}" class="font-medium text-amber-600 hover:underline">{{EMAIL}}</a>
          </div>
          <div>
            <span class="text-xs uppercase font-bold text-gray-400 block">Verified Business Line</span>
            <a href="tel:{{PHONE}}" class="font-medium text-slate-800 hover:underline">{{PHONE}}</a>
          </div>
          <div>
            <span class="text-xs uppercase font-bold text-gray-400 block">Registered Corporate Office</span>
            <span class="text-gray-700 leading-relaxed">{{ADDRESS}}</span>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- LEGAL & PRIVACY POLICY -->
  <section id="compliance" class="py-16 px-6 max-w-5xl mx-auto">
    <div class="bg-white p-8 rounded-xl border border-gray-200 shadow-sm text-xs text-gray-500 space-y-4">
      <h3 class="text-sm font-bold text-slate-900 uppercase tracking-wide">Privacy Notice & Business Terms</h3>
      <p>
        This portal is operated by <strong>{{BUSINESS_NAME}}</strong>. All communications, inquiries, phone calls, and technical project scopes received through this site are utilized strictly for estimating projects, executing civil construction contracts, and maintaining official corporate records.
      </p>
      <p>
        For regulatory inspections, formal vendor audits, or GST documentation verification, contact our administrative department at <strong>{{EMAIL}}</strong> or visit our office at <strong>{{ADDRESS}}</strong>.
      </p>
    </div>
  </section>

  <!-- CONTACT SECTION -->
  <section id="contact" class="bg-slate-900 text-white py-24 px-6">
    <div class="max-w-7xl mx-auto grid md:grid-cols-2 gap-12">
      <div>
        <span class="text-amber-400 font-bold uppercase tracking-wider text-xs">Direct Channel</span>
        <h2 class="text-3xl md:text-4xl font-black mb-6">Contact Registered Office</h2>
        <p class="text-gray-400 text-sm mb-8">
          Reach out for tender inquiries, BOQ estimations, structural consults, or formal corporate contracts.
        </p>

        <div class="space-y-6 text-sm">
          <div class="flex items-start space-x-4">
            <div class="w-10 h-10 rounded bg-slate-800 flex items-center justify-center text-amber-400 flex-shrink-0 mt-1">
              <i class="fa-solid fa-location-dot"></i>
            </div>
            <div>
              <span class="block text-gray-400 text-xs font-semibold uppercase">Physical Office</span>
              <span class="text-gray-200 font-medium leading-relaxed">{{ADDRESS}}</span>
            </div>
          </div>

          <div class="flex items-start space-x-4">
            <div class="w-10 h-10 rounded bg-slate-800 flex items-center justify-center text-amber-400 flex-shrink-0 mt-1">
              <i class="fa-solid fa-envelope"></i>
            </div>
            <div>
              <span class="block text-gray-400 text-xs font-semibold uppercase">Official Email</span>
              <a href="mailto:{{EMAIL}}" class="text-amber-400 hover:underline">{{EMAIL}}</a>
            </div>
          </div>

          <div class="flex items-start space-x-4">
            <div class="w-10 h-10 rounded bg-slate-800 flex items-center justify-center text-amber-400 flex-shrink-0 mt-1">
              <i class="fa-solid fa-phone"></i>
            </div>
            <div>
              <span class="block text-gray-400 text-xs font-semibold uppercase">Telephone Line</span>
              <a href="tel:{{PHONE}}" class="text-gray-200 hover:underline">{{PHONE}}</a>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-slate-800 p-8 rounded-xl border border-slate-700 shadow-xl">
        <h3 class="text-xl font-bold mb-4">Request Project Quote</h3>
        <form onsubmit="event.preventDefault(); alert('Inquiry recorded. Contracting team will revert within 24 hours.');" class="space-y-4 text-sm">
          <div>
            <label class="block text-gray-300 mb-1 text-xs">Full Name / Entity Name</label>
            <input type="text" required class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2.5 text-white focus:outline-none focus:border-amber-400">
          </div>
          <div>
            <label class="block text-gray-300 mb-1 text-xs">Phone Number</label>
            <input type="tel" required class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2.5 text-white focus:outline-none focus:border-amber-400">
          </div>
          <div>
            <label class="block text-gray-300 mb-1 text-xs">Project Scope</label>
            <textarea rows="3" required class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2.5 text-white focus:outline-none focus:border-amber-400"></textarea>
          </div>
          <button type="submit" class="w-full bg-amber-500 hover:bg-amber-600 text-slate-950 font-bold py-3 rounded transition shadow">Send Inquiry</button>
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
        <a href="#compliance" class="hover:underline">Terms & Conditions</a>
        <a href="#contact" class="hover:underline">Contact Office</a>
      </div>
    </div>
  </footer>

  <!-- LOGIN MODAL -->
  <div id="loginModal" class="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 hidden items-center justify-center p-4">
    <div class="bg-slate-900 border border-slate-700 w-full max-w-md p-6 rounded-xl shadow-2xl relative text-white">
      <button onclick="closeModal('loginModal')" class="absolute top-4 right-4 text-gray-400 hover:text-white text-xl">
        <i class="fa-solid fa-xmark"></i>
      </button>
      <h3 class="text-xl font-bold mb-1">Client Portal Login</h3>
      <p class="text-xs text-gray-400 mb-6">Access your project BOQ, blueprints, and milestone status</p>
      <form onsubmit="event.preventDefault(); alert('Authentication portal active. Access restricted to registered site clients.');" class="space-y-4 text-sm">
        <div>
          <label class="block text-gray-400 text-xs mb-1">Registered Email</label>
          <input type="email" required class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-white focus:outline-none focus:border-amber-500">
        </div>
        <div>
          <label class="block text-gray-400 text-xs mb-1">Password</label>
          <input type="password" required class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-white focus:outline-none focus:border-amber-500">
        </div>
        <button type="submit" class="w-full bg-amber-500 hover:bg-amber-600 text-slate-950 font-bold py-2.5 rounded transition">Sign In</button>
      </form>
    </div>
  </div>

  <!-- REGISTER MODAL -->
  <div id="registerModal" class="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 hidden items-center justify-center p-4">
    <div class="bg-slate-900 border border-slate-700 w-full max-w-md p-6 rounded-xl shadow-2xl relative text-white">
      <button onclick="closeModal('registerModal')" class="absolute top-4 right-4 text-gray-400 hover:text-white text-xl">
        <i class="fa-solid fa-xmark"></i>
      </button>
      <h3 class="text-xl font-bold mb-1">New Client Registration</h3>
      <p class="text-xs text-gray-400 mb-6">Register your company details to receive official project estimates</p>
      <form onsubmit="event.preventDefault(); alert('Registration recorded. Profile activation will be dispatched to your email.');" class="space-y-4 text-sm">
        <div>
          <label class="block text-gray-400 text-xs mb-1">Client / Company Name</label>
          <input type="text" required class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-white focus:outline-none focus:border-amber-500">
        </div>
        <div>
          <label class="block text-gray-400 text-xs mb-1">Official Email</label>
          <input type="email" required class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-white focus:outline-none focus:border-amber-500">
        </div>
        <div>
          <label class="block text-gray-400 text-xs mb-1">Set Password</label>
          <input type="password" required class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-white focus:outline-none focus:border-amber-500">
        </div>
        <button type="submit" class="w-full bg-amber-500 hover:bg-amber-600 text-slate-950 font-bold py-2.5 rounded transition">Register Account</button>
      </form>
    </div>
  </div>

  <!-- SCRIPT FOR MODALS -->
  <script>
    function openModal(id) {
      document.getElementById(id).classList.add('modal-active');
    }
    function closeModal(id) {
      document.getElementById(id).classList.remove('modal-active');
    }
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
        "🏗️ *Construction Website Generator Bot*\n\n"
        "Mujhe niche diye format me details bhejo, mai turant ready `index.html` file bana kar bhej dunga:\n\n"
        "`Name: Shree Balaji Construction`\n"
        "`Email: contact@example.com`\n"
        "`Phone: +91 9876543210`\n"
        "`Address: Shop 12, Main Market, Indore, MP 452001`\n"
        "`Year: 2019`\n\n"
        "_(Copy karke bas apni details replace karo aur bhej do)_"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    data = parse_details(message.text)
    
    # Check if required fields exist
    if not all(k in data for k in ["name", "email", "phone", "address"]):
        bot.reply_to(
            message,
            "⚠️ *Kripya sahi format me bhejein!*\n\n"
            "Format:\n"
            "`Name: Company Name`\n"
            "`Email: your@email.com`\n"
            "`Phone: +919876543210`\n"
            "`Address: Full Address Here`\n"
            "`Year: 2020` *(Optional)*",
            parse_mode="Markdown"
        )
        return

    year = data.get("year", "2019")
    
    # Generate HTML by replacing all placeholders safely
    html_output = HTML_TEMPLATE
    html_output = html_output.replace("{{BUSINESS_NAME}}", data["name"])
    html_output = html_output.replace("{{EMAIL}}", data["email"])
    html_output = html_output.replace("{{PHONE}}", data["phone"])
    html_output = html_output.replace("{{ADDRESS}}", data["address"])
    html_output = html_output.replace("{{YEAR}}", year)

    # Prepare file as in-memory document
    file_bytes = io.BytesIO(html_output.encode("utf-8"))
    file_bytes.name = "index.html"

    clean_filename = re.sub(r'[^a-zA-Z0-9]', '_', data["name"]).lower() + "_index.html"
    file_bytes.name = clean_filename

    caption = (
        f"✅ *Website HTML Ready!*\n\n"
        f"🏢 *Entity:* {data['name']}\n"
        f"📧 *Email:* {data['email']}\n"
        f"📞 *Phone:* {data['phone']}\n"
        f"📍 *Address:* {data['address']}\n\n"
        f"👉 Is file ko download karke Vercel par direct drop karo."
    )

    bot.send_document(
        chat_id=message.chat.id,
        document=file_bytes,
        caption=caption,
        parse_mode="Markdown"
    )

if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()
