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
  <title>{{BUSINESS_NAME}} | Building Construction & Civil Infrastructure</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    body { font-family: 'Plus Jakarta Sans', sans-serif; }
    .modal-active { display: flex !important; }
    
    /* Live Video & Continuous Motion Animation */
    @keyframes slowZoom {
      0% { transform: scale(1); }
      50% { transform: scale(1.12); }
      100% { transform: scale(1); }
    }
    .animate-live-bg {
      animation: slowZoom 22s infinite ease-in-out;
    }
    .hover-lift {
      transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .hover-lift:hover {
      transform: translateY(-8px);
      box-shadow: 0 20px 35px -10px rgba(234, 88, 12, 0.2);
    }
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
<body class="bg-white text-slate-900 antialiased selection:bg-orange-600 selection:text-white">

  <!-- 1. TOP BAR -->
  <div class="bg-slate-900 text-slate-200 text-xs py-2.5 px-6 border-b border-slate-800">
    <div class="max-w-7xl mx-auto flex flex-wrap justify-between items-center gap-2">
      <div class="flex items-center space-x-6">
        <a href="tel:{{PHONE}}" class="hover:text-orange-400 transition flex items-center">
          <i class="fa-solid fa-phone-volume text-orange-500 mr-2"></i> {{PHONE}}
        </a>
        <a href="mailto:{{EMAIL}}" class="hidden sm:flex hover:text-orange-400 transition items-center">
          <i class="fa-solid fa-envelope text-orange-500 mr-2"></i> {{EMAIL}}
        </a>
        <span class="hidden lg:flex items-center text-slate-400">
          <i class="fa-solid fa-location-dot text-orange-500 mr-2"></i> {{ADDRESS}}
        </span>
      </div>
      <div class="flex items-center space-x-4">
        <span class="text-emerald-400 font-semibold flex items-center">
          <i class="fa-solid fa-circle-check mr-1.5"></i> ISO 9001:2015 Certified Builder
        </span>
        <span class="text-slate-700">|</span>
        <button onclick="openModal('loginModal')" class="text-white hover:text-orange-400 font-semibold transition">Login</button>
        <button onclick="openModal('signupModal')" class="bg-orange-600 hover:bg-orange-500 text-white px-3 py-1 rounded font-bold transition">Sign Up</button>
      </div>
    </div>
  </div>

  <!-- 2. STICKY WHITE NAVBAR -->
  <header class="bg-white/95 backdrop-blur-md sticky top-0 z-40 border-b border-gray-200 shadow-sm">
    <div class="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
      <a href="#" class="flex items-center space-x-3 group">
        <div class="w-11 h-11 rounded-xl bg-orange-600 flex items-center justify-center text-white text-xl shadow-md shadow-orange-600/30 group-hover:bg-slate-900 transition">
          <i class="fa-solid fa-trowel-bricks"></i>
        </div>
        <div>
          <span class="text-xl md:text-2xl font-extrabold tracking-tight text-slate-900 block leading-none">{{BUSINESS_NAME}}</span>
          <span class="text-[10px] font-bold uppercase tracking-widest text-orange-600">Buildings & Civil Construction</span>
        </div>
      </a>

      <nav class="hidden xl:flex items-center space-x-7 text-sm font-bold text-slate-700">
        <a href="#about" class="hover:text-orange-600 transition">About Us</a>
        <a href="#services" class="hover:text-orange-600 transition">Services</a>
        <a href="#ongoing" class="hover:text-orange-600 transition">Ongoing Sites</a>
        <a href="#completed" class="hover:text-orange-600 transition">Completed Buildings</a>
        <a href="#workforce" class="hover:text-orange-600 transition">Our Workforce</a>
        <a href="#process" class="hover:text-orange-600 transition">Process</a>
        <a href="#contact" class="hover:text-orange-600 transition">Contact</a>
      </nav>

      <div class="flex items-center space-x-3">
        <button onclick="openModal('loginModal')" class="hidden sm:inline-flex items-center px-4 py-2.5 border-2 border-slate-900 text-slate-900 hover:bg-slate-900 hover:text-white rounded-lg text-xs font-extrabold uppercase tracking-wider transition">
          <i class="fa-regular fa-user mr-2"></i> Log In
        </button>
        <button onclick="openModal('signupModal')" class="inline-flex items-center px-5 py-2.5 bg-orange-600 hover:bg-orange-700 text-white rounded-lg text-xs font-extrabold uppercase tracking-wider shadow-lg shadow-orange-600/25 transition">
          Sign Up
        </button>
      </div>
    </div>
  </header>

  <!-- 3. HERO SECTION WITH LIVE VIDEO BACKGROUND -->
  <section class="relative min-h-[88vh] flex items-center justify-center overflow-hidden bg-slate-900">
    <!-- Animated Fallback Layer + Live HTML5 Video -->
    <div class="absolute inset-0 overflow-hidden z-0">
      <img src="https://images.unsplash.com/photo-1541888946425-d09bb18086f6?auto=format&fit=crop&w=1920&q=85" alt="Construction Site" class="w-full h-full object-cover animate-live-bg opacity-45">
      <video autoplay loop muted playsinline class="absolute inset-0 w-full h-full object-cover opacity-65">
        <source src="https://cdn.pixabay.com/video/2020/05/25/40130-424930032_large.mp4" type="video/mp4">
        <source src="https://assets.mixkit.co/videos/preview/mixkit-construction-site-of-a-modern-building-41004-large.mp4" type="video/mp4">
      </video>
    </div>

    <div class="absolute inset-0 bg-gradient-to-r from-slate-950/90 via-slate-900/75 to-slate-900/40 z-10"></div>

    <div class="relative z-20 max-w-7xl mx-auto px-6 py-20 grid lg:grid-cols-12 gap-12 items-center w-full">
      <div class="lg:col-span-8 text-white">
        <div class="inline-flex items-center gap-2 bg-orange-600/90 text-white px-4 py-1.5 rounded-full text-xs font-extrabold uppercase tracking-wider mb-6 shadow-lg">
          <span class="w-2 h-2 rounded-full bg-white animate-ping"></span>
          <span>Live On-Site Civil Engineering & Turnkey Construction</span>
        </div>

        <h1 class="text-4xl sm:text-6xl lg:text-7xl font-black tracking-tight leading-none mb-6 uppercase">
          {{BUSINESS_NAME}}
        </h1>

        <div class="text-xl sm:text-2xl md:text-3xl font-bold text-orange-400 mb-6 min-h-[40px]">
          <span>We Build: </span>
          <span id="typewriter" class="text-white typing-cursor">Residential & Commercial High-Rise Towers</span>
        </div>

        <p class="text-base md:text-lg text-slate-200 max-w-2xl mb-10 leading-relaxed">
          From deep foundation excavation and RCC structural framing to complete architectural finishing. We construct high-strength residential apartments, commercial complexes, and industrial buildings with 300+ active site workers and modern machinery.
        </p>

        <div class="flex flex-wrap gap-4">
          <a href="#ongoing" class="bg-orange-600 hover:bg-orange-500 text-white font-extrabold px-8 py-4 rounded-xl shadow-xl transition transform hover:-translate-y-1 flex items-center">
            <i class="fa-solid fa-helmet-safety mr-2.5 text-lg"></i> View Live Construction Sites
          </a>
          <a href="#contact" class="bg-white hover:bg-gray-100 text-slate-900 font-extrabold px-8 py-4 rounded-xl shadow-xl transition transform hover:-translate-y-1 flex items-center">
            <i class="fa-solid fa-phone-volume mr-2.5 text-orange-600"></i> Contact Head Office
          </a>
        </div>
      </div>

      <!-- Hero Right Quick Estimate Card -->
      <div class="lg:col-span-4 bg-white text-slate-900 p-8 rounded-2xl shadow-2xl border-t-4 border-orange-600">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-xl font-extrabold">Free Construction Quote</h3>
          <span class="bg-orange-100 text-orange-700 text-xs font-bold px-2.5 py-1 rounded">24 Hr Reply</span>
        </div>
        <p class="text-xs text-slate-500 mb-6">Get an instant bill of quantities (BOQ) and structural cost estimate for your plot or commercial project.</p>
        <form onsubmit="event.preventDefault(); alert('Thank you! Our Senior Site Engineer from {{BUSINESS_NAME}} will call you shortly.');" class="space-y-4 text-sm">
          <div>
            <label class="block text-xs font-bold uppercase text-slate-600 mb-1">Your Full Name</label>
            <input type="text" required placeholder="Enter your name" class="w-full bg-gray-50 border border-gray-300 rounded-lg px-4 py-2.5 focus:outline-none focus:border-orange-600">
          </div>
          <div>
            <label class="block text-xs font-bold uppercase text-slate-600 mb-1">Phone Number</label>
            <input type="tel" required placeholder="+91 XXXXX XXXXX" class="w-full bg-gray-50 border border-gray-300 rounded-lg px-4 py-2.5 focus:outline-none focus:border-orange-600">
          </div>
          <div>
            <label class="block text-xs font-bold uppercase text-slate-600 mb-1">Building Category</label>
            <select class="w-full bg-gray-50 border border-gray-300 rounded-lg px-4 py-2.5 focus:outline-none focus:border-orange-600 font-medium">
              <option>Commercial Building / Plaza</option>
              <option>Residential Apartment / Villa</option>
              <option>RCC Framed Structure Only</option>
              <option>Industrial Warehouse / Factory</option>
            </select>
          </div>
          <button type="submit" class="w-full bg-slate-900 hover:bg-orange-600 text-white font-extrabold py-3.5 rounded-lg transition shadow-md">
            Calculate Construction Cost
          </button>
        </form>
      </div>
    </div>
  </section>

  <!-- 4. TRUST STATS COUNTER STRIP -->
  <section class="bg-orange-600 text-white py-12 px-6 shadow-inner">
    <div class="max-w-7xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-8 text-center divide-x divide-orange-500/40">
      <div>
        <div class="text-4xl md:text-5xl font-black mb-1">165+</div>
        <div class="text-xs uppercase font-bold tracking-widest text-orange-100">Completed Buildings</div>
      </div>
      <div>
        <div class="text-4xl md:text-5xl font-black mb-1">28</div>
        <div class="text-xs uppercase font-bold tracking-widest text-orange-100">Ongoing Active Sites</div>
      </div>
      <div>
        <div class="text-4xl md:text-5xl font-black mb-1">450+</div>
        <div class="text-xs uppercase font-bold tracking-widest text-orange-100">Skilled Workers & Engineers</div>
      </div>
      <div>
        <div class="text-4xl md:text-5xl font-black mb-1">4.2M</div>
        <div class="text-xs uppercase font-bold tracking-widest text-orange-100">Sq. Ft. Area Constructed</div>
      </div>
    </div>
  </section>

  <!-- 5. ABOUT US & WORKERS ON SITE -->
  <section id="about" class="py-24 px-6 max-w-7xl mx-auto">
    <div class="grid lg:grid-cols-2 gap-16 items-center">
      <div class="grid grid-cols-2 gap-4 relative">
        <div class="space-y-4">
          <img src="https://images.unsplash.com/photo-1504307651254-35680f356dfd?auto=format&fit=crop&w=700&q=80" alt="Construction Workers" class="rounded-2xl shadow-lg h-64 w-full object-cover hover-lift">
          <img src="https://images.unsplash.com/photo-1590674899484-d5640e854abe?auto=format&fit=crop&w=700&q=80" alt="Unfinished Building" class="rounded-2xl shadow-lg h-56 w-full object-cover hover-lift">
        </div>
        <div class="space-y-4 pt-8">
          <img src="https://images.unsplash.com/photo-1541888946425-d09bb18086f6?auto=format&fit=crop&w=700&q=80" alt="Site Engineers" class="rounded-2xl shadow-lg h-56 w-full object-cover hover-lift">
          <img src="https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=700&q=80" alt="Completed Building" class="rounded-2xl shadow-lg h-64 w-full object-cover hover-lift">
        </div>
        <div class="absolute -bottom-6 left-1/2 -translate-x-1/2 bg-slate-900 text-white px-6 py-4 rounded-xl shadow-2xl border-l-4 border-orange-500 flex items-center space-x-4 w-11/12 sm:w-auto">
          <i class="fa-solid fa-award text-3xl text-orange-500"></i>
          <div>
            <div class="font-extrabold text-sm">A-Grade Licensed Civil Contractor</div>
            <div class="text-xs text-slate-400">100% Earthquake Resistant IS-456 RCC Standards</div>
          </div>
        </div>
      </div>

      <div>
        <span class="text-orange-600 font-extrabold uppercase tracking-widest text-xs bg-orange-50 px-3 py-1.5 rounded-full">About {{BUSINESS_NAME}}</span>
        <h2 class="text-3xl md:text-5xl font-black text-slate-900 mt-4 mb-6 leading-tight">
          Transforming Blueprints Into Landmark Concrete Structures
        </h2>
        <p class="text-slate-600 text-base leading-relaxed mb-6">
          <strong>{{BUSINESS_NAME}}</strong> is a premier building construction and civil engineering company headquartered at <strong>{{ADDRESS}}</strong>. We specialize in end-to-end execution of multi-story residential complexes, corporate towers, institutional buildings, and heavy industrial structures.
        </p>
        <p class="text-slate-600 text-sm leading-relaxed mb-8">
          Every project is supervised by experienced structural engineers, architects, and dedicated site supervisors. We use only lab-tested Fe-550D TMT steel bars, M25/M30 grade ready-mix concrete (RMC), and advanced laser leveling tools.
        </p>

        <div class="grid sm:grid-cols-2 gap-4 mb-8">
          <div class="flex items-start space-x-3 p-4 rounded-xl bg-gray-50 border border-gray-200">
            <i class="fa-solid fa-Hard-hat fa-helmet-safety text-orange-600 text-xl mt-1"></i>
            <div>
              <h4 class="font-bold text-slate-900 text-sm">Dedicated Site Workforce</h4>
              <p class="text-xs text-slate-500 mt-1">Trained masons, bar-benders, shuttering carpenters & site engineers.</p>
            </div>
          </div>
          <div class="flex items-start space-x-3 p-4 rounded-xl bg-gray-50 border border-gray-200">
            <i class="fa-solid fa-building-shield text-orange-600 text-xl mt-1"></i>
            <div>
              <h4 class="font-bold text-slate-900 text-sm">On-Time Possession</h4>
              <p class="text-xs text-slate-500 mt-1">Milestone-based tracking from foundation digging to key handover.</p>
            </div>
          </div>
        </div>

        <div class="flex flex-wrap items-center gap-6 pt-4 border-t border-gray-200">
          <div>
            <span class="text-xs text-slate-400 uppercase font-bold block">Direct Helpline</span>
            <a href="tel:{{PHONE}}" class="text-lg font-extrabold text-slate-900 hover:text-orange-600">{{PHONE}}</a>
          </div>
          <div class="h-8 w-px bg-gray-300 hidden sm:block"></div>
          <div>
            <span class="text-xs text-slate-400 uppercase font-bold block">Official Email</span>
            <a href="mailto:{{EMAIL}}" class="text-lg font-extrabold text-orange-600 hover:underline">{{EMAIL}}</a>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 6. ONGOING PROJECTS ("ADHURI BUILDINGS" / UNDER CONSTRUCTION) -->
  <section id="ongoing" class="py-24 bg-gray-50 border-y border-gray-200 px-6">
    <div class="max-w-7xl mx-auto">
      <div class="flex flex-col md:flex-row justify-between items-end mb-16 gap-6">
        <div>
          <span class="text-orange-600 font-extrabold uppercase tracking-widest text-xs bg-orange-100 px-3 py-1.5 rounded-full">Live Construction Sites</span>
          <h2 class="text-3xl md:text-5xl font-black text-slate-900 mt-3">Ongoing Under-Construction Buildings</h2>
          <p class="text-slate-600 text-sm mt-2 max-w-2xl">Real-time progress of our active building structures currently undergoing RCC slab casting, brickwork, and exterior elevation.</p>
        </div>
        <a href="#contact" class="bg-slate-900 hover:bg-orange-600 text-white text-xs font-extrabold uppercase tracking-wider px-6 py-3.5 rounded-xl transition">
          Book Site Visit <i class="fa-solid fa-arrow-right ml-2"></i>
        </a>
      </div>

      <div class="grid md:grid-cols-3 gap-8">
        <!-- Adhuri Building 1 -->
        <div class="bg-white rounded-2xl overflow-hidden border border-gray-200 shadow-md hover-lift">
          <div class="relative h-64 overflow-hidden">
            <img src="https://images.unsplash.com/photo-1590674899484-d5640e854abe?auto=format&fit=crop&w=800&q=80" alt="Under Construction RCC Building" class="w-full h-full object-cover">
            <span class="absolute top-4 left-4 bg-amber-500 text-slate-950 text-xs font-extrabold uppercase px-3 py-1 rounded-full shadow">
              <i class="fa-solid fa-spinner fa-spin mr-1"></i> Under Construction
            </span>
            <span class="absolute bottom-4 right-4 bg-slate-900/90 text-white text-xs font-bold px-3 py-1 rounded">
              G + 12 Floors
            </span>
          </div>
          <div class="p-6">
            <h3 class="text-xl font-extrabold text-slate-900 mb-2">Skyline Commercial Arcade</h3>
            <p class="text-xs text-slate-500 mb-4">RCC column & 8th-floor slab shuttering in progress. Tower crane and 65 workers currently deployed on site.</p>
            <div class="mb-2 flex justify-between text-xs font-bold">
              <span class="text-slate-700">Structural Progress (RCC & Masonry)</span>
              <span class="text-orange-600">68% Completed</span>
            </div>
            <div class="w-full bg-gray-200 h-2.5 rounded-full overflow-hidden">
              <div class="bg-orange-600 h-full rounded-full" style="width: 68%"></div>
            </div>
          </div>
        </div>

        <!-- Adhuri Building 2 -->
        <div class="bg-white rounded-2xl overflow-hidden border border-gray-200 shadow-md hover-lift">
          <div class="relative h-64 overflow-hidden">
            <img src="https://images.unsplash.com/photo-1508450859948-4e04fabaa4ea?auto=format&fit=crop&w=800&q=80" alt="High Rise Scaffolding" class="w-full h-full object-cover">
            <span class="absolute top-4 left-4 bg-amber-500 text-slate-950 text-xs font-extrabold uppercase px-3 py-1 rounded-full shadow">
              <i class="fa-solid fa-spinner fa-spin mr-1"></i> Structure Stage
            </span>
            <span class="absolute bottom-4 right-4 bg-slate-900/90 text-white text-xs font-bold px-3 py-1 rounded">
              G + 18 Towers
            </span>
          </div>
          <div class="p-6">
            <h3 class="text-xl font-extrabold text-slate-900 mb-2">Green Valley Residency Phase-II</h3>
            <p class="text-xs text-slate-500 mb-4">Brickwork, internal plastering, and external scaffolding erection active across Wing A and Wing B.</p>
            <div class="mb-2 flex justify-between text-xs font-bold">
              <span class="text-slate-700">Brickwork & Plastering Stage</span>
              <span class="text-orange-600">82% Completed</span>
            </div>
            <div class="w-full bg-gray-200 h-2.5 rounded-full overflow-hidden">
              <div class="bg-orange-600 h-full rounded-full" style="width: 82%"></div>
            </div>
          </div>
        </div>

        <!-- Adhuri Building 3 -->
        <div class="bg-white rounded-2xl overflow-hidden border border-gray-200 shadow-md hover-lift">
          <div class="relative h-64 overflow-hidden">
            <img src="https://images.unsplash.com/photo-1531834685032-c34bf0d84c77?auto=format&fit=crop&w=800&q=80" alt="Foundation & Steel Binding" class="w-full h-full object-cover">
            <span class="absolute top-4 left-4 bg-amber-500 text-slate-950 text-xs font-extrabold uppercase px-3 py-1 rounded-full shadow">
              <i class="fa-solid fa-spinner fa-spin mr-1"></i> Foundation & Plinth
            </span>
            <span class="absolute bottom-4 right-4 bg-slate-900/90 text-white text-xs font-bold px-3 py-1 rounded">
              Industrial Park
            </span>
          </div>
          <div class="p-6">
            <h3 class="text-xl font-extrabold text-slate-900 mb-2">Metro Logistics & Corporate Hub</h3>
            <p class="text-xs text-slate-500 mb-4">Deep raft foundation, heavy TMT steel reinforcement binding, and plinth beam concrete pouring underway.</p>
            <div class="mb-2 flex justify-between text-xs font-bold">
              <span class="text-slate-700">Foundation & Plinth Level</span>
              <span class="text-orange-600">45% Completed</span>
            </div>
            <div class="w-full bg-gray-200 h-2.5 rounded-full overflow-hidden">
              <div class="bg-orange-600 h-full rounded-full" style="width: 45%"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 7. COMPLETED PROJECTS ("BANI HUI BUILDINGS" / READY LANDMARKS) -->
  <section id="completed" class="py-24 px-6 max-w-7xl mx-auto">
    <div class="text-center mb-16">
      <span class="text-emerald-700 font-extrabold uppercase tracking-widest text-xs bg-emerald-100 px-3 py-1.5 rounded-full">100% Delivered Portfolio</span>
      <h2 class="text-3xl md:text-5xl font-black text-slate-900 mt-3">Completed & Handed-Over Buildings</h2>
      <p class="text-slate-600 text-sm mt-2 max-w-2xl mx-auto">Explore our successfully constructed and occupied residential towers, corporate offices, and commercial plazas.</p>
    </div>

    <div class="grid md:grid-cols-3 gap-8">
      <!-- Bani Building 1 -->
      <div class="bg-white rounded-2xl overflow-hidden border border-gray-200 shadow-lg hover-lift group">
        <div class="relative h-72 overflow-hidden">
          <img src="https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=800&q=80" alt="Completed Corporate Tower" class="w-full h-full object-cover group-hover:scale-110 transition duration-500">
          <span class="absolute top-4 left-4 bg-emerald-600 text-white text-xs font-extrabold uppercase px-3 py-1 rounded-full shadow">
            <i class="fa-solid fa-check-circle mr-1"></i> Completed & Occupied
          </span>
        </div>
        <div class="p-6">
          <span class="text-xs font-bold text-orange-600 uppercase">Commercial High-Rise</span>
          <h3 class="text-xl font-extrabold text-slate-900 mt-1 mb-2">Apex Pinnacle Corporate Tower</h3>
          <p class="text-xs text-slate-500 mb-4">14-story glass facade commercial building with 2-level basement parking and high-speed elevators.</p>
          <div class="pt-4 border-t border-gray-100 flex justify-between text-xs font-bold text-slate-600">
            <span><i class="fa-solid fa-vector-square text-orange-600 mr-1"></i> 1,45,000 Sq.Ft.</span>
            <span><i class="fa-solid fa-calendar-check text-emerald-600 mr-1"></i> Handed Over</span>
          </div>
        </div>
      </div>

      <!-- Bani Building 2 -->
      <div class="bg-white rounded-2xl overflow-hidden border border-gray-200 shadow-lg hover-lift group">
        <div class="relative h-72 overflow-hidden">
          <img src="https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=800&q=80" alt="Completed Residential Apartment" class="w-full h-full object-cover group-hover:scale-110 transition duration-500">
          <span class="absolute top-4 left-4 bg-emerald-600 text-white text-xs font-extrabold uppercase px-3 py-1 rounded-full shadow">
            <i class="fa-solid fa-check-circle mr-1"></i> Completed & Occupied
          </span>
        </div>
        <div class="p-6">
          <span class="text-xs font-bold text-orange-600 uppercase">Luxury Residential Society</span>
          <h3 class="text-xl font-extrabold text-slate-900 mt-1 mb-2">Royal Heritage Apartments</h3>
          <p class="text-xs text-slate-500 mb-4">120 luxury 3BHK & 4BHK residential flats with clubhouse, earthquake-resistant RCC frame, and landscaped podium.</p>
          <div class="pt-4 border-t border-gray-100 flex justify-between text-xs font-bold text-slate-600">
            <span><i class="fa-solid fa-vector-square text-orange-600 mr-1"></i> 2,10,000 Sq.Ft.</span>
            <span><i class="fa-solid fa-calendar-check text-emerald-600 mr-1"></i> Handed Over</span>
          </div>
        </div>
      </div>

      <!-- Bani Building 3 -->
      <div class="bg-white rounded-2xl overflow-hidden border border-gray-200 shadow-lg hover-lift group">
        <div class="relative h-72 overflow-hidden">
          <img src="https://images.unsplash.com/photo-1577495508048-b635879837f1?auto=format&fit=crop&w=800&q=80" alt="Completed Business Park" class="w-full h-full object-cover group-hover:scale-110 transition duration-500">
          <span class="absolute top-4 left-4 bg-emerald-600 text-white text-xs font-extrabold uppercase px-3 py-1 rounded-full shadow">
            <i class="fa-solid fa-check-circle mr-1"></i> Completed & Occupied
          </span>
        </div>
        <div class="p-6">
          <span class="text-xs font-bold text-orange-600 uppercase">Retail & Office Complex</span>
          <h3 class="text-xl font-extrabold text-slate-900 mt-1 mb-2">Imperial Trade Center</h3>
          <p class="text-xs text-slate-500 mb-4">Turnkey civil, structural, electrical, and HVAC execution for a multi-brand retail & corporate hub.</p>
          <div class="pt-4 border-t border-gray-100 flex justify-between text-xs font-bold text-slate-600">
            <span><i class="fa-solid fa-vector-square text-orange-600 mr-1"></i> 95,000 Sq.Ft.</span>
            <span><i class="fa-solid fa-calendar-check text-emerald-600 mr-1"></i> Handed Over</span>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 8. OUR WORKFORCE & SITE ENGINEERS ("WORKERS KA PHOTO" SECTION) -->
  <section id="workforce" class="py-24 bg-slate-900 text-white px-6">
    <div class="max-w-7xl mx-auto">
      <div class="text-center mb-16">
        <span class="text-orange-400 font-extrabold uppercase tracking-widest text-xs bg-orange-500/10 border border-orange-500/30 px-3 py-1.5 rounded-full">Our Strength On Ground</span>
        <h2 class="text-3xl md:text-5xl font-black mt-3">Engineers, Masons & On-Site Workforce</h2>
        <p class="text-slate-400 text-sm mt-2 max-w-2xl mx-auto">Behind every strong building stands our disciplined team of civil engineers, site supervisors, crane operators, and skilled construction workers.</p>
      </div>

      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div class="bg-slate-800 rounded-2xl overflow-hidden border border-slate-700 hover-lift">
          <img src="https://images.unsplash.com/photo-1504307651254-35680f356dfd?auto=format&fit=crop&w=600&q=80" alt="Site Workers Team" class="w-full h-60 object-cover">
          <div class="p-5">
            <span class="text-orange-400 text-[11px] font-bold uppercase">Structural Execution</span>
            <h4 class="font-extrabold text-lg mt-1">RCC & Shuttering Workforce</h4>
            <p class="text-xs text-slate-400 mt-1">200+ certified bar-benders, form-work carpenters, and concrete masons.</p>
          </div>
        </div>

        <div class="bg-slate-800 rounded-2xl overflow-hidden border border-slate-700 hover-lift">
          <img src="https://images.unsplash.com/photo-1581094794329-c8112a89af12?auto=format&fit=crop&w=600&q=80" alt="Civil Engineers" class="w-full h-60 object-cover">
          <div class="p-5">
            <span class="text-orange-400 text-[11px] font-bold uppercase">Quality & Blueprint</span>
            <h4 class="font-extrabold text-lg mt-1">Chief Civil Engineers</h4>
            <p class="text-xs text-slate-400 mt-1">On-site structural inspection, Theodolite surveying, and cube strength testing.</p>
          </div>
        </div>

        <div class="bg-slate-800 rounded-2xl overflow-hidden border border-slate-700 hover-lift">
          <img src="https://images.unsplash.com/photo-1541888946425-d09bb18086f6?auto=format&fit=crop&w=600&q=80" alt="Safety Supervisors" class="w-full h-60 object-cover">
          <div class="p-5">
            <span class="text-orange-400 text-[11px] font-bold uppercase">Zero Accident Policy</span>
            <h4 class="font-extrabold text-lg mt-1">Site Safety Officers</h4>
            <p class="text-xs text-slate-400 mt-1">Strict PPE helmet, harness, and scaffolding safety compliance across all floors.</p>
          </div>
        </div>

        <div class="bg-slate-800 rounded-2xl overflow-hidden border border-slate-700 hover-lift">
          <img src="https://images.unsplash.com/photo-1503387762-592deb58ef4e?auto=format&fit=crop&w=600&q=80" alt="Finishing Crew" class="w-full h-60 object-cover">
          <div class="p-5">
            <span class="text-orange-400 text-[11px] font-bold uppercase">MEP & Elevation</span>
            <h4 class="font-extrabold text-lg mt-1">Finishing & MEP Technicians</h4>
            <p class="text-xs text-slate-400 mt-1">Expert teams for electrical conduiting, plumbing, glazing, and facade work.</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 9. CORE BUILDING SERVICES -->
  <section id="services" class="py-24 px-6 max-w-7xl mx-auto">
    <div class="text-center mb-16">
      <span class="text-orange-600 font-extrabold uppercase tracking-widest text-xs bg-orange-50 px-3 py-1.5 rounded-full">What We Do</span>
      <h2 class="text-3xl md:text-5xl font-black text-slate-900 mt-3">Complete Building Construction Services</h2>
    </div>

    <div class="grid md:grid-cols-3 gap-8">
      <div class="bg-white p-8 rounded-2xl border border-gray-200 shadow-sm hover-lift">
        <div class="w-14 h-14 rounded-xl bg-orange-100 text-orange-600 flex items-center justify-center text-2xl mb-6">
          <i class="fa-solid fa-building"></i>
        </div>
        <h3 class="text-xl font-extrabold text-slate-900 mb-3">Turnkey Building Construction</h3>
        <p class="text-slate-600 text-sm leading-relaxed">Complete with-material construction from architectural map approval and soil testing to final interior finishing and handover.</p>
      </div>

      <div class="bg-white p-8 rounded-2xl border border-gray-200 shadow-sm hover-lift">
        <div class="w-14 h-14 rounded-xl bg-orange-100 text-orange-600 flex items-center justify-center text-2xl mb-6">
          <i class="fa-solid fa-layer-group"></i>
        </div>
        <h3 class="text-xl font-extrabold text-slate-900 mb-3">RCC Framed Structures</h3>
        <p class="text-slate-600 text-sm leading-relaxed">High-load bearing deep pile foundations, columns, beams, and multi-story RCC slab casting using M30 Ready-Mix Concrete.</p>
      </div>

      <div class="bg-white p-8 rounded-2xl border border-gray-200 shadow-sm hover-lift">
        <div class="w-14 h-14 rounded-xl bg-orange-100 text-orange-600 flex items-center justify-center text-2xl mb-6">
          <i class="fa-solid fa-warehouse"></i>
        </div>
        <h3 class="text-xl font-extrabold text-slate-900 mb-3">Commercial & Industrial Sheds</h3>
        <p class="text-slate-600 text-sm leading-relaxed">Shopping malls, hospitals, schools, cold storages, and heavy pre-engineered steel buildings (PEB) with VDF flooring.</p>
      </div>

      <div class="bg-white p-8 rounded-2xl border border-gray-200 shadow-sm hover-lift">
        <div class="w-14 h-14 rounded-xl bg-orange-100 text-orange-600 flex items-center justify-center text-2xl mb-6">
          <i class="fa-solid fa-compass-drafting"></i>
        </div>
        <h3 class="text-xl font-extrabold text-slate-900 mb-3">3D Elevation & Structural Design</h3>
        <p class="text-slate-600 text-sm leading-relaxed">2D CAD floor plans, 3D front elevations, structural steel detailing, and municipal building permit clearances.</p>
      </div>

      <div class="bg-white p-8 rounded-2xl border border-gray-200 shadow-sm hover-lift">
        <div class="w-14 h-14 rounded-xl bg-orange-100 text-orange-600 flex items-center justify-center text-2xl mb-6">
          <i class="fa-solid fa-truck-monster"></i>
        </div>
        <h3 class="text-xl font-extrabold text-slate-900 mb-3">Excavation & Earthwork</h3>
        <p class="text-slate-600 text-sm leading-relaxed">Basement digging, rock breaking, land leveling, anti-termite treatment, and PCC sub-base preparation with heavy JCB & Poclain fleet.</p>
      </div>

      <div class="bg-white p-8 rounded-2xl border border-gray-200 shadow-sm hover-lift">
        <div class="w-14 h-14 rounded-xl bg-orange-100 text-orange-600 flex items-center justify-center text-2xl mb-6">
          <i class="fa-solid fa-paint-roller"></i>
        </div>
        <h3 class="text-xl font-extrabold text-slate-900 mb-3">Plaster, Waterproofing & Finishing</h3>
        <p class="text-slate-600 text-sm leading-relaxed">Double-coat exterior sand-faced plaster, chemical terrace waterproofing, vitrified flooring, and ACP glass glazing.</p>
      </div>
    </div>
  </section>

  <!-- 10. 6-STEP CONSTRUCTION PROCESS -->
  <section id="process" class="py-20 bg-gray-50 border-y border-gray-200 px-6">
    <div class="max-w-7xl mx-auto">
      <div class="text-center mb-16">
        <span class="text-orange-600 font-extrabold uppercase tracking-widest text-xs">How We Work</span>
        <h2 class="text-3xl md:text-4xl font-black text-slate-900 mt-2">6-Stage Building Execution Roadmap</h2>
      </div>

      <div class="grid sm:grid-cols-2 lg:grid-cols-6 gap-6">
        <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
          <div class="text-2xl font-black text-orange-600 mb-2">01</div>
          <h4 class="font-bold text-slate-900 text-sm mb-1">Soil Test & Map</h4>
          <p class="text-xs text-slate-500">Land survey, soil bearing capacity test & 3D structural drawing.</p>
        </div>
        <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
          <div class="text-2xl font-black text-orange-600 mb-2">02</div>
          <h4 class="font-bold text-slate-900 text-sm mb-1">Excavation & Footing</h4>
          <p class="text-xs text-slate-500">Deep pit excavation, PCC bed, and heavy RCC foundation footings.</p>
        </div>
        <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
          <div class="text-2xl font-black text-orange-600 mb-2">03</div>
          <h4 class="font-bold text-slate-900 text-sm mb-1">Plinth & Superstructure</h4>
          <p class="text-xs text-slate-500">Plinth beam casting, column raising, and multi-floor RCC slabs.</p>
        </div>
        <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
          <div class="text-2xl font-black text-orange-600 mb-2">04</div>
          <h4 class="font-bold text-slate-900 text-sm mb-1">Brickwork & MEP</h4>
          <p class="text-xs text-slate-500">AAC block / red brick masonry, concealed plumbing & electrical lines.</p>
        </div>
        <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
          <div class="text-2xl font-black text-orange-600 mb-2">05</div>
          <h4 class="font-bold text-slate-900 text-sm mb-1">Plaster & Flooring</h4>
          <p class="text-xs text-slate-500">Internal/external plastering, waterproofing, granite & tile fixing.</p>
        </div>
        <div class="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
          <div class="text-2xl font-black text-orange-600 mb-2">06</div>
          <h4 class="font-bold text-slate-900 text-sm mb-1">Final Handover</h4>
          <p class="text-xs text-slate-500">Painting, glass facade, quality audit & completion certificate.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- 11. REGISTERED COMPANY VERIFICATION TABLE -->
  <section class="py-20 px-6 max-w-5xl mx-auto">
    <div class="bg-white border-2 border-slate-900 rounded-2xl p-8 shadow-xl">
      <div class="flex flex-wrap items-center justify-between gap-4 pb-6 mb-6 border-b border-gray-200">
        <div>
          <span class="text-xs font-extrabold uppercase tracking-widest text-orange-600">Statutory Corporate Disclosure</span>
          <h3 class="text-2xl font-black text-slate-900">Verified Legal Entity Information</h3>
        </div>
        <span class="bg-emerald-100 text-emerald-800 text-xs font-extrabold px-4 py-1.5 rounded-full flex items-center">
          <i class="fa-solid fa-shield-check mr-2"></i> Active Registered Business
        </span>
      </div>

      <div class="grid md:grid-cols-2 gap-6 text-sm">
        <div class="p-4 bg-gray-50 rounded-xl border border-gray-200">
          <span class="text-xs font-bold uppercase text-slate-400 block mb-1">Registered Company Name</span>
          <span class="text-base font-extrabold text-slate-900">{{BUSINESS_NAME}}</span>
        </div>
        <div class="p-4 bg-gray-50 rounded-xl border border-gray-200">
          <span class="text-xs font-bold uppercase text-slate-400 block mb-1">Business Category</span>
          <span class="text-base font-extrabold text-slate-900">Building Construction & Civil Contracting</span>
        </div>
        <div class="p-4 bg-gray-50 rounded-xl border border-gray-200">
          <span class="text-xs font-bold uppercase text-slate-400 block mb-1">Registered Telephone Number</span>
          <a href="tel:{{PHONE}}" class="text-base font-extrabold text-orange-600 hover:underline">{{PHONE}}</a>
        </div>
        <div class="p-4 bg-gray-50 rounded-xl border border-gray-200">
          <span class="text-xs font-bold uppercase text-slate-400 block mb-1">Official Corporate Email</span>
          <a href="mailto:{{EMAIL}}" class="text-base font-extrabold text-orange-600 hover:underline">{{EMAIL}}</a>
        </div>
        <div class="md:col-span-2 p-4 bg-gray-50 rounded-xl border border-gray-200">
          <span class="text-xs font-bold uppercase text-slate-400 block mb-1">Registered Head Office Address</span>
          <span class="text-base font-extrabold text-slate-900">{{ADDRESS}}</span>
        </div>
      </div>
    </div>
  </section>

  <!-- 12. CONTACT SECTION & FOOTER WITH MANDATORY DETAILS -->
  <section id="contact" class="bg-slate-900 text-white pt-20 pb-12 px-6 border-t-4 border-orange-600">
    <div class="max-w-7xl mx-auto grid lg:grid-cols-12 gap-12 pb-16 border-b border-slate-800">
      <div class="lg:col-span-5">
        <div class="flex items-center space-x-3 mb-6">
          <div class="w-10 h-10 rounded-lg bg-orange-600 flex items-center justify-center text-white text-lg font-black">
            <i class="fa-solid fa-trowel-bricks"></i>
          </div>
          <span class="text-2xl font-black tracking-tight text-white">{{BUSINESS_NAME}}</span>
        </div>
        <p class="text-slate-400 text-sm leading-relaxed mb-8">
          Trusted civil engineering and building construction contractors delivering high-rise residential, commercial, and industrial infrastructure projects.
        </p>
        <div class="flex space-x-4">
          <button onclick="openModal('loginModal')" class="bg-slate-800 hover:bg-orange-600 text-white text-xs font-bold px-5 py-2.5 rounded-lg transition">Client Portal Login</button>
          <button onclick="openModal('signupModal')" class="bg-orange-600 hover:bg-orange-500 text-white text-xs font-bold px-5 py-2.5 rounded-lg transition">Vendor Sign Up</button>
        </div>
      </div>

      <!-- Highlighted Address, Phone, Email Cards -->
      <div class="lg:col-span-7 grid sm:grid-cols-3 gap-6">
        <div class="bg-slate-800/90 p-6 rounded-2xl border border-slate-700">
          <div class="w-10 h-10 rounded-lg bg-orange-600/20 text-orange-400 flex items-center justify-center text-lg mb-4">
            <i class="fa-solid fa-location-dot"></i>
          </div>
          <h4 class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">Office Address</h4>
          <p class="text-sm font-bold text-white leading-relaxed">{{ADDRESS}}</p>
        </div>

        <div class="bg-slate-800/90 p-6 rounded-2xl border border-slate-700">
          <div class="w-10 h-10 rounded-lg bg-orange-600/20 text-orange-400 flex items-center justify-center text-lg mb-4">
            <i class="fa-solid fa-phone-volume"></i>
          </div>
          <h4 class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">Phone Number</h4>
          <a href="tel:{{PHONE}}" class="text-base font-extrabold text-orange-400 hover:underline block">{{PHONE}}</a>
          <span class="text-[11px] text-slate-400 mt-1 block">Mon-Sat (9 AM - 7 PM)</span>
        </div>

        <div class="bg-slate-800/90 p-6 rounded-2xl border border-slate-700">
          <div class="w-10 h-10 rounded-lg bg-orange-600/20 text-orange-400 flex items-center justify-center text-lg mb-4">
            <i class="fa-solid fa-envelope"></i>
          </div>
          <h4 class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">Official Email</h4>
          <a href="mailto:{{EMAIL}}" class="text-sm font-extrabold text-orange-400 hover:underline break-all block">{{EMAIL}}</a>
          <span class="text-[11px] text-slate-400 mt-1 block">24/7 Tender Desk</span>
        </div>
      </div>
    </div>

    <div class="max-w-7xl mx-auto pt-8 flex flex-col sm:flex-row justify-between items-center text-xs text-slate-400 gap-4">
      <p>© 2026 <strong>{{BUSINESS_NAME}}</strong>. All Rights Reserved. | Address: {{ADDRESS}} | Phone: {{PHONE}} | Email: {{EMAIL}}</p>
      <div class="flex space-x-6">
        <a href="#about" class="hover:text-white">Privacy Policy</a>
        <a href="#about" class="hover:text-white">Terms & Conditions</a>
      </div>
    </div>
  </section>

  <!-- LOGIN MODAL WITH GOOGLE SIGN-IN -->
  <div id="loginModal" class="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 hidden items-center justify-center p-4">
    <div class="bg-white text-slate-900 w-full max-w-md p-8 rounded-2xl shadow-2xl relative border border-gray-200">
      <button onclick="closeModal('loginModal')" class="absolute top-5 right-5 text-slate-400 hover:text-slate-900 text-xl">
        <i class="fa-solid fa-xmark"></i>
      </button>
      <h3 class="text-2xl font-black mb-1">Client Portal Login</h3>
      <p class="text-xs text-slate-500 mb-6">Sign in to view your building progress & BOQ invoices</p>

      <button onclick="alert('Connecting to Google Account for {{BUSINESS_NAME}}...');" class="w-full bg-white hover:bg-gray-50 text-slate-800 font-bold py-3 px-4 rounded-xl border border-gray-300 flex items-center justify-center space-x-3 mb-5 transition shadow-sm">
        <svg class="w-5 h-5" viewBox="0 0 24 24">
          <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
          <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
          <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
          <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
        </svg>
        <span class="text-sm">Continue with Google</span>
      </button>

      <div class="flex items-center my-4">
        <div class="flex-grow border-t border-gray-200"></div>
        <span class="px-3 text-xs text-slate-400 font-bold uppercase">Or Email Login</span>
        <div class="flex-grow border-t border-gray-200"></div>
      </div>

      <form onsubmit="event.preventDefault(); alert('Logged in check initiated. Redirecting to client dashboard...');" class="space-y-4 text-sm">
        <div>
          <label class="block text-xs font-bold text-slate-700 mb-1">Email Address</label>
          <input type="email" required placeholder="name@company.com" class="w-full bg-gray-50 border border-gray-300 rounded-xl px-4 py-2.5 focus:outline-none focus:border-orange-600">
        </div>
        <div>
          <label class="block text-xs font-bold text-slate-700 mb-1">Password</label>
          <input type="password" required placeholder="••••••••" class="w-full bg-gray-50 border border-gray-300 rounded-xl px-4 py-2.5 focus:outline-none focus:border-orange-600">
        </div>
        <button type="submit" class="w-full bg-orange-600 hover:bg-orange-700 text-white font-extrabold py-3 rounded-xl transition shadow-md">
          Log In to Account
        </button>
      </form>
    </div>
  </div>

  <!-- SIGN UP MODAL WITH GOOGLE SIGN-IN -->
  <div id="signupModal" class="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 hidden items-center justify-center p-4">
    <div class="bg-white text-slate-900 w-full max-w-md p-8 rounded-2xl shadow-2xl relative border border-gray-200">
      <button onclick="closeModal('signupModal')" class="absolute top-5 right-5 text-slate-400 hover:text-slate-900 text-xl">
        <i class="fa-solid fa-xmark"></i>
      </button>
      <h3 class="text-2xl font-black mb-1">Create New Account</h3>
      <p class="text-xs text-slate-500 mb-6">Register as a Client or Material Contractor with {{BUSINESS_NAME}}</p>

      <button onclick="alert('Google Sign-Up initiated for {{BUSINESS_NAME}}...');" class="w-full bg-white hover:bg-gray-50 text-slate-800 font-bold py-3 px-4 rounded-xl border border-gray-300 flex items-center justify-center space-x-3 mb-5 transition shadow-sm">
        <svg class="w-5 h-5" viewBox="0 0 24 24">
          <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
          <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
          <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
          <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
        </svg>
        <span class="text-sm">Sign up with Google</span>
      </button>

      <form onsubmit="event.preventDefault(); alert('Registration successful! Verification email sent.');" class="space-y-3.5 text-sm">
        <div>
          <label class="block text-xs font-bold text-slate-700 mb-1">Full Name / Company Name</label>
          <input type="text" required placeholder="Enter full name" class="w-full bg-gray-50 border border-gray-300 rounded-xl px-4 py-2.5 focus:outline-none focus:border-orange-600">
        </div>
        <div>
          <label class="block text-xs font-bold text-slate-700 mb-1">Mobile Number</label>
          <input type="tel" required placeholder="+91 98765 43210" class="w-full bg-gray-50 border border-gray-300 rounded-xl px-4 py-2.5 focus:outline-none focus:border-orange-600">
        </div>
        <div>
          <label class="block text-xs font-bold text-slate-700 mb-1">Email Address</label>
          <input type="email" required placeholder="you@domain.com" class="w-full bg-gray-50 border border-gray-300 rounded-xl px-4 py-2.5 focus:outline-none focus:border-orange-600">
        </div>
        <div>
          <label class="block text-xs font-bold text-slate-700 mb-1">Create Password</label>
          <input type="password" required placeholder="Create strong password" class="w-full bg-gray-50 border border-gray-300 rounded-xl px-4 py-2.5 focus:outline-none focus:border-orange-600">
        </div>
        <button type="submit" class="w-full bg-slate-900 hover:bg-orange-600 text-white font-extrabold py-3 rounded-xl transition shadow-md">
          Create Free Account
        </button>
      </form>
    </div>
  </div>

  <script>
    function openModal(id) { document.getElementById(id).classList.add('modal-active'); }
    function closeModal(id) { document.getElementById(id).classList.remove('modal-active'); }

    const phrases = [
      "Residential & Commercial High-Rise Towers",
      "Earthquake-Resistant RCC Framed Structures",
      "Turnkey Industrial Warehouses & Plazas",
      "Modern Luxury Apartments & Corporate Hubs"
    ];
    let pIndex = 0, cIndex = 0, deleting = false;
    const el = document.getElementById("typewriter");

    function typeLoop() {
      const current = phrases[pIndex];
      el.innerText = deleting ? current.substring(0, cIndex--) : current.substring(0, cIndex++);
      let speed = deleting ? 35 : 70;
      if (!deleting && cIndex > current.length) { speed = 2000; deleting = true; }
      else if (deleting && cIndex === 0) { deleting = false; pIndex = (pIndex + 1) % phrases.length; speed = 400; }
      setTimeout(typeLoop, speed);
    }
    document.addEventListener("DOMContentLoaded", typeLoop);
  </script>
</body>
</html>
"""

def parse_details(text):
    data = {}
    for line in text.strip().split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            k, v = k.strip().lower(), v.strip()
            if "name" in k:
                data["name"] = v
            elif "email" in k or "gmail" in k or "mail" in k:
                data["email"] = v
            elif "phone" in k or "mobile" in k or "number" in k:
                data["phone"] = v
            elif "address" in k or "location" in k:
                data["address"] = v
    return data

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    msg = (
        "🏗️ *White-Theme Building Construction Website Generator*\n\n"
        "Details is format me bhejo:\n\n"
        "`Name: Shivam Building Constructions`\n"
        "`Phone: +91 9876543210`\n"
        "`Email: info@heoo.in`\n"
        "`Address: Plot 45, Civil Lines, Kanpur, UP 208001`"
    )
    bot.reply_to(message, msg, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def generate_site(message):
    data = parse_details(message.text)
    if not all(k in data for k in ["name", "phone", "email", "address"]):
        bot.reply_to(
            message,
            "⚠️ *Saari 4 details bhejo:*\n\n"
            "`Name: Business Name`\n"
            "`Phone: +91 9876543210`\n"
            "`Email: contact@heoo.in`\n"
            "`Address: Full Office Address`",
            parse_mode="Markdown"
        )
        return

    html = (
        HTML_TEMPLATE
        .replace("{{BUSINESS_NAME}}", data["name"])
        .replace("{{PHONE}}", data["phone"])
        .replace("{{EMAIL}}", data["email"])
        .replace("{{ADDRESS}}", data["address"])
    )

    bio = io.BytesIO(html.encode("utf-8"))
    bio.name = "index.html"

    bot.send_document(
        message.chat.id,
        bio,
        caption=(
            f"✅ *Building Construction Website Ready!*\n\n"
            f"🏢 *Name:* {data['name']}\n"
            f"📞 *Phone:* {data['phone']}\n"
            f"📧 *Email:* {data['email']}\n"
            f"📍 *Address:* {data['address']}"
        ),
        parse_mode="Markdown"
    )

app = Flask(__name__)

@app.route('/')
def health():
    return "Construction Bot Live 24/7"

if __name__ == "__main__":
    threading.Thread(
        target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080))),
        daemon=True
    ).start()
    try:
        bot.remove_webhook()
    except Exception:
        pass
    bot.infinity_polling(timeout=20, long_polling_timeout=20)
