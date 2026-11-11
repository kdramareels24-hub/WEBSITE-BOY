import os
import re
import io
import threading
from flask import Flask
import telebot

BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
bot = telebot.TeleBot(BOT_TOKEN)

# DIALECT/LAYOUT 1: CONSTRUCTION & INFRASTRUCTURE
CONSTRUCTION_HTML = """<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{BUSINESS_NAME}} | Civil Engineering & Infra</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  <style>
    .modal-active { display: flex !important; }
    .video-bg { position: absolute; top: 50%; left: 50%; min-width: 100%; min-height: 100%; width: auto; height: auto; transform: translateX(-50%) translateY(-50%); object-fit: cover; }
  </style>
</head>
<body class="bg-slate-950 text-slate-100 font-sans">
  <header class="fixed top-0 w-full z-50 bg-slate-900/90 backdrop-blur border-b border-amber-500/30 px-6 py-4 flex justify-between items-center">
    <span class="text-xl font-black text-amber-500">{{BUSINESS_NAME}}</span>
    <button onclick="document.getElementById('loginModal').classList.add('modal-active')" class="bg-amber-500 text-slate-950 px-4 py-2 rounded font-bold text-sm">Client Login</button>
  </header>
  
  <section class="relative h-screen flex items-center justify-center overflow-hidden">
    <video autoplay loop muted playsinline class="video-bg opacity-30">
      <source src="https://assets.mixkit.co/videos/preview/mixkit-construction-site-of-a-modern-building-41004-large.mp4" type="video/mp4">
    </video>
    <div class="relative z-10 text-center px-4 max-w-4xl mx-auto">
      <h1 class="text-5xl md:text-7xl font-black mb-6 uppercase tracking-wider">{{BUSINESS_NAME}}</h1>
      <p class="text-xl text-amber-400 mb-8 font-semibold">Heavy Civil Construction & Infrastructure Development</p>
      <div class="flex justify-center gap-4">
        <a href="#contact" class="bg-amber-500 hover:bg-amber-600 text-slate-950 px-8 py-4 rounded font-black text-lg transition">Enquire Now</a>
      </div>
    </div>
  </section>

  <!-- MULTIPLE SECTIONS TO INCREASE SCROLL LENGTH -->
  <div class="py-20 max-w-7xl mx-auto px-6 space-y-20">
    <div><h2 class="text-3xl font-bold mb-4 border-l-4 border-amber-500 pl-4">About Our Engineering</h2><p class="text-slate-400 leading-relaxed">Providing absolute structural integrity and certified civil execution across industrial, commercial, and residential sectors.</p></div>
    <div><h2 class="text-3xl font-bold mb-4 border-l-4 border-amber-500 pl-4">Core Verticals</h2><div class="grid md:grid-cols-3 gap-6"><div class="bg-slate-900 p-6 rounded border border-slate-800"><h3 class="font-bold text-xl mb-2">RCC Framework</h3><p class="text-slate-400 text-sm">High-grade reinforced cement concrete structures built to endure extreme environmental stress.</p></div><div class="bg-slate-900 p-6 rounded border border-slate-800"><h3 class="font-bold text-xl mb-2">Commercial Hubs</h3><p class="text-slate-400 text-sm">Turnkey execution of corporate plazas, retail centers, and multi-story business parks.</p></div><div class="bg-slate-900 p-6 rounded border border-slate-800"><h3 class="font-bold text-xl mb-2">Industrial Sheds</h3><p class="text-slate-400 text-sm">Pre-engineered steel buildings designed for heavy manufacturing and logistics operations.</p></div></div></div>
    <div><h2 class="text-3xl font-bold mb-4 border-l-4 border-amber-500 pl-4">Quality Assurance</h2><p class="text-slate-400 leading-relaxed">Every metric ton of steel and every batch of concrete undergoes rigorous non-destructive testing before installation.</p></div>
    <div><h2 class="text-3xl font-bold mb-4 border-l-4 border-amber-500 pl-4">Active Fleet Deployment</h2><p class="text-slate-400 leading-relaxed">Equipped with state-of-the-art batching plants, tower cranes, and earth-moving machinery for rapid project delivery.</p></div>
    <div><h2 class="text-3xl font-bold mb-4 border-l-4 border-amber-500 pl-4">Sustainability Mandate</h2><p class="text-slate-400 leading-relaxed">Integrating eco-friendly construction practices and waste reduction protocols across all active job sites.</p></div>
    <div><h2 class="text-3xl font-bold mb-4 border-l-4 border-amber-500 pl-4">Client Portfolio</h2><p class="text-slate-400 leading-relaxed">Trusted partner for government bodies, multinational corporations, and private real estate developers.</p></div>
    <div><h2 class="text-3xl font-bold mb-4 border-l-4 border-amber-500 pl-4">Safety Protocols</h2><p class="text-slate-400 leading-relaxed">Zero-incident policy enforced through mandatory PPE compliance and daily safety briefings.</p></div>
    <div><h2 class="text-3xl font-bold mb-4 border-l-4 border-amber-500 pl-4">Project Management</h2><p class="text-slate-400 leading-relaxed">Utilizing advanced scheduling software to guarantee timely handover within strict budgetary constraints.</p></div>
  </div>

  <section id="contact" class="bg-slate-900 py-20 px-6 border-t border-slate-800">
    <div class="max-w-4xl mx-auto text-center">
      <h2 class="text-4xl font-extrabold mb-6">Official Corporate Desk</h2>
      <div class="space-y-4 text-slate-300 mb-8 border border-slate-800 p-6 rounded bg-slate-950 inline-block text-left min-w-full md:min-w-[500px]">
        <div><strong class="text-amber-500">Address:</strong> {{ADDRESS}}</div>
        <div><strong class="text-amber-500">Phone:</strong> {{PHONE}}</div>
        <div><strong class="text-amber-500">Email:</strong> {{EMAIL}}</div>
      </div>
    </div>
  </section>

  <footer class="bg-black text-slate-500 text-xs py-8 text-center border-t border-slate-900">
    <p>© 2026 {{BUSINESS_NAME}}. All Rights Reserved.</p>
  </footer>

  <div id="loginModal" class="fixed inset-0 bg-black/80 z-50 hidden items-center justify-center p-4">
    <div class="bg-slate-900 border border-slate-700 w-full max-w-md p-6 rounded relative text-white">
      <button onclick="document.getElementById('loginModal').classList.remove('modal-active')" class="absolute top-4 right-4 text-slate-400 hover:text-white"><i class="fa-solid fa-xmark"></i></button>
      <h3 class="text-xl font-bold mb-4">Client Portal</h3>
      <button class="w-full bg-white text-black font-bold py-2 px-4 rounded mb-4 flex items-center justify-center gap-2"><i class="fa-brands fa-google text-red-500"></i> Continue with Google</button>
      <form onsubmit="event.preventDefault();" class="space-y-4">
        <input type="email" placeholder="Email" class="w-full bg-slate-800 border-slate-700 border p-2 rounded text-white">
        <input type="password" placeholder="Password" class="w-full bg-slate-800 border-slate-700 border p-2 rounded text-white">
        <button type="submit" class="w-full bg-amber-500 text-slate-950 font-bold py-2 rounded">Sign In</button>
      </form>
    </div>
  </div>
</body>
</html>
"""

# DIALECT/LAYOUT 2: TRAVEL & TOURISM
TRAVEL_HTML = """<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{BUSINESS_NAME}} | Global Travel & Tours</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  <style>.modal-active { display: flex !important; } .video-bg { position: absolute; top: 50%; left: 50%; min-width: 100%; min-height: 100%; width: auto; height: auto; transform: translateX(-50%) translateY(-50%); object-fit: cover; }</style>
</head>
<body class="bg-sky-50 text-slate-800 font-sans">
  <nav class="fixed top-0 w-full z-50 bg-white/90 backdrop-blur shadow-md px-6 py-4 flex justify-between items-center">
    <span class="text-2xl font-black text-sky-600"><i class="fa-solid fa-plane-departure mr-2"></i>{{BUSINESS_NAME}}</span>
    <button onclick="document.getElementById('loginModal').classList.add('modal-active')" class="bg-sky-600 text-white px-4 py-2 rounded font-bold text-sm">Member Sign In</button>
  </nav>

  <section class="relative h-screen flex items-center justify-center overflow-hidden">
    <video autoplay loop muted playsinline class="video-bg opacity-20">
      <source src="https://assets.mixkit.co/videos/preview/mixkit-aerial-view-of-a-tropical-beach-4428-large.mp4" type="video/mp4">
    </video>
    <div class="relative z-10 text-center px-4 max-w-4xl mx-auto">
      <h1 class="text-6xl md:text-8xl font-black text-slate-900 mb-6 drop-shadow">{{BUSINESS_NAME}}</h1>
      <p class="text-2xl text-sky-800 font-bold mb-8">Curated Global Expeditions & Luxury Travel Management</p>
      <a href="#contact" class="bg-sky-600 text-white px-10 py-5 rounded-full font-black text-lg shadow-lg hover:bg-sky-700 transition inline-block">Book Your Journey</a>
    </div>
  </section>

  <div class="py-24 max-w-7xl mx-auto px-6 space-y-16">
    <div class="text-center"><h2 class="text-4xl font-black text-slate-900 mb-4">Explore the Unknown</h2><p class="text-slate-600 max-w-2xl mx-auto">We redefine exploration through bespoke itineraries, VIP concierge services, and seamless global routing.</p></div>
    <div class="grid md:grid-cols-4 gap-6"><div class="bg-white p-6 shadow rounded text-center"><i class="fa-solid fa-passport text-3xl text-sky-600 mb-4"></i><h4 class="font-bold mb-2">Visa Assistance</h4><p class="text-xs text-slate-500">End-to-end documentation processing.</p></div><div class="bg-white p-6 shadow rounded text-center"><i class="fa-solid fa-hotel text-3xl text-sky-600 mb-4"></i><h4 class="font-bold mb-2">Luxury Stays</h4><p class="text-xs text-slate-500">Partnered with elite resorts worldwide.</p></div><div class="bg-white p-6 shadow rounded text-center"><i class="fa-solid fa-plane-up text-3xl text-sky-600 mb-4"></i><h4 class="font-bold mb-2">Charter Flights</h4><p class="text-xs text-slate-500">Private aviation for discerning travelers.</p></div><div class="bg-white p-6 shadow rounded text-center"><i class="fa-solid fa-shield-heart text-3xl text-sky-600 mb-4"></i><h4 class="font-bold mb-2">Global Insurance</h4><p class="text-xs text-slate-500">Comprehensive travel protection.</p></div></div>
    <div><h3 class="text-2xl font-bold mb-2">Destinations</h3><p class="text-slate-600">From the Swiss Alps to the beaches of Bali, our reach spans over 140 countries with dedicated local guides ensuring authentic cultural immersion.</p></div>
    <div><h3 class="text-2xl font-bold mb-2">Corporate Travel</h3><p class="text-slate-600">Specialized corporate booking portals designed to streamline business travel management with consolidated billing and automated policy compliance.</p></div>
    <div><h3 class="text-2xl font-bold mb-2">Adventure Tourism</h3><p class="text-slate-600">High-adrenaline expeditions led by certified mountaineers and survival experts ensuring maximum safety during extreme trekking.</p></div>
    <div><h3 class="text-2xl font-bold mb-2">Cultural Heritage Tours</h3><p class="text-slate-600">Private access to historical monuments and exclusive lectures by renowned historians across global heritage sites.</p></div>
    <div><h3 class="text-2xl font-bold mb-2">Culinary Trails</h3><p class="text-slate-600">Gastronomic journeys featuring Michelin-starred dining experiences and private masterclasses with celebrated local chefs.</p></div>
    <div><h3 class="text-2xl font-bold mb-2">Wellness Retreats</h3><p class="text-slate-600">Rejuvenating escapes focused on holistic health, featuring Ayurvedic treatments, meditation sessions, and spa therapies.</p></div>
  </div>

  <section id="contact" class="bg-slate-900 text-white py-20 px-6">
    <div class="max-w-3xl mx-auto text-center">
      <h2 class="text-3xl font-bold mb-6">Concierge Contact Desk</h2>
      <div class="bg-slate-800 p-8 rounded shadow-inner text-left space-y-4">
        <div><strong>Physical Location:</strong> {{ADDRESS}}</div>
        <div><strong>Direct Line:</strong> {{PHONE}}</div>
        <div><strong>Electronic Mail:</strong> {{EMAIL}}</div>
      </div>
    </div>
  </section>

  <footer class="bg-slate-100 text-slate-400 text-xs py-6 text-center">© 2026 {{BUSINESS_NAME}}. All Rights Reserved.</footer>

  <div id="loginModal" class="fixed inset-0 bg-black/60 z-50 hidden items-center justify-center p-4">
    <div class="bg-white w-full max-w-md p-6 rounded shadow-xl text-slate-800 relative">
      <button onclick="document.getElementById('loginModal').classList.remove('modal-active')" class="absolute top-4 right-4 text-slate-400"><i class="fa-solid fa-xmark"></i></button>
      <h3 class="text-xl font-bold mb-4">Traveler Sign In</h3>
      <button class="w-full border border-slate-300 font-bold py-2 px-4 rounded mb-4 flex items-center justify-center gap-2"><i class="fa-brands fa-google text-red-500"></i> Continue with Google</button>
      <form onsubmit="event.preventDefault();" class="space-y-4">
        <input type="email" placeholder="Email Address" class="w-full border-slate-300 border p-2 rounded">
        <input type="password" placeholder="Password" class="w-full border-slate-300 border p-2 rounded">
        <button type="submit" class="w-full bg-sky-600 text-white font-bold py-2 rounded">Log In</button>
      </form>
    </div>
  </div>
</body>
</html>
"""

# DIALECT/LAYOUT 3: GROCERY & RETAIL
GROCERY_HTML = """<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{BUSINESS_NAME}} | Fresh & Organic Market</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  <style>.modal-active { display: flex !important; } .video-bg { position: absolute; top: 50%; left: 50%; min-width: 100%; min-height: 100%; width: auto; height: auto; transform: translateX(-50%) translateY(-50%); object-fit: cover; }</style>
</head>
<body class="bg-emerald-50 text-slate-800 font-sans">
  <header class="sticky top-0 z-50 bg-emerald-600 text-white shadow p-4 flex justify-between items-center">
    <h1 class="text-2xl font-black"><i class="fa-solid fa-basket-shopping mr-2"></i>{{BUSINESS_NAME}}</h1>
    <button onclick="document.getElementById('loginModal').classList.add('modal-active')" class="bg-emerald-800 px-4 py-2 rounded font-bold text-sm">Account</button>
  </header>
  
  <section class="relative h-[80vh] flex items-center justify-center overflow-hidden">
    <video autoplay loop muted playsinline class="video-bg opacity-30">
      <source src="https://assets.mixkit.co/videos/preview/mixkit-hands-holding-a-basket-full-of-fresh-vegetables-42587-large.mp4" type="video/mp4">
    </video>
    <div class="relative z-10 text-center px-4 max-w-4xl mx-auto">
      <h2 class="text-5xl md:text-7xl font-black text-emerald-950 mb-4">{{BUSINESS_NAME}}</h2>
      <p class="text-xl font-bold bg-white/80 backdrop-blur inline-block px-6 py-2 rounded text-emerald-800 mb-6">Farm to Table Essentials Delivered Daily</p>
      <div><a href="#contact" class="bg-emerald-600 text-white px-8 py-4 rounded font-bold">Visit Store</a></div>
    </div>
  </section>

  <div class="py-16 max-w-7xl mx-auto px-6 space-y-12">
    <div class="grid md:grid-cols-4 gap-6 text-center"><div class="bg-white p-6 rounded"><i class="fa-solid fa-truck text-2xl text-emerald-600 mb-2"></i><h4 class="font-bold">Fast Delivery</h4></div><div class="bg-white p-6 rounded"><i class="fa-solid fa-apple-whole text-2xl text-emerald-600 mb-2"></i><h4 class="font-bold">100% Organic</h4></div><div class="bg-white p-6 rounded"><i class="fa-solid fa-tag text-2xl text-emerald-600 mb-2"></i><h4 class="font-bold">Best Prices</h4></div><div class="bg-white p-6 rounded"><i class="fa-solid fa-certificate text-2xl text-emerald-600 mb-2"></i><h4 class="font-bold">ISO Certified</h4></div></div>
    <div><h3 class="text-xl font-bold mb-2">Fresh Produce</h3><p>Sourced directly from regional agrarian collectives to ensure maximum retention of nutritional value and flavor profiles.</p></div>
    <div><h3 class="text-xl font-bold mb-2">Dairy & Bakery</h3><p>Artisanal breads baked daily and dairy products free from synthetic hormones and artificial preservatives.</p></div>
    <div><h3 class="text-xl font-bold mb-2">Pantry Staples</h3><p>A comprehensive inventory of grains, pulses, oils, and spices meeting rigorous quality control standards.</p></div>
    <div><h3 class="text-xl font-bold mb-2">Household Supplies</h3><p>Eco-friendly cleaning agents and personal care products safe for family environments.</p></div>
    <div><h3 class="text-xl font-bold mb-2">Gourmet Selection</h3><p>Imported delicacies and specialty ingredients catering to international culinary requirements.</p></div>
    <div><h3 class="text-xl font-bold mb-2">Customer Loyalty</h3><p>Reward programs offering substantial discounts and priority delivery slots for frequent patrons.</p></div>
  </div>

  <section id="contact" class="bg-emerald-900 text-white py-16 px-6 text-center">
    <h3 class="text-3xl font-bold mb-4">Retail Location Details</h3>
    <div class="max-w-md mx-auto space-y-2 text-emerald-200">
      <div><strong>Address:</strong> {{ADDRESS}}</div>
      <div><strong>Helpline:</strong> {{PHONE}}</div>
      <div><strong>Support Mail:</strong> {{EMAIL}}</div>
    </div>
  </section>

  <footer class="bg-emerald-950 text-emerald-600 text-xs py-4 text-center">© 2026 {{BUSINESS_NAME}}. All Rights Reserved.</footer>

  <div id="loginModal" class="fixed inset-0 bg-black/60 z-50 hidden items-center justify-center p-4">
    <div class="bg-white w-full max-w-md p-6 rounded text-slate-800 relative">
      <button onclick="document.getElementById('loginModal').classList.remove('modal-active')" class="absolute top-4 right-4"><i class="fa-solid fa-xmark"></i></button>
      <h3 class="text-xl font-bold mb-4">Customer Login</h3>
      <button class="w-full border p-2 rounded mb-4 font-bold flex items-center justify-center gap-2"><i class="fa-brands fa-google text-red-500"></i> Continue with Google</button>
      <form onsubmit="event.preventDefault();" class="space-y-4">
        <input type="email" placeholder="Email" class="w-full border p-2 rounded">
        <input type="password" placeholder="Password" class="w-full border p-2 rounded">
        <button type="submit" class="w-full bg-emerald-600 text-white font-bold py-2 rounded">Login</button>
      </form>
    </div>
  </div>
</body>
</html>
"""

# DIALECT/LAYOUT 4: BROADCASTING & MEDIA
BROADCASTING_HTML = """<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{BUSINESS_NAME}} | Media & Broadcasting</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  <style>.modal-active { display: flex !important; } .video-bg { position: absolute; top: 50%; left: 50%; min-width: 100%; min-height: 100%; width: auto; height: auto; transform: translateX(-50%) translateY(-50%); object-fit: cover; }</style>
</head>
<body class="bg-purple-950 text-white font-mono">
  <nav class="fixed top-0 w-full z-50 bg-black/90 border-b border-purple-500/50 p-4 flex justify-between items-center">
    <span class="text-2xl font-black text-purple-400 tracking-tighter">{{BUSINESS_NAME}}</span>
    <button onclick="document.getElementById('loginModal').classList.add('modal-active')" class="bg-purple-600 px-4 py-2 text-xs font-bold uppercase rounded">Producer Login</button>
  </nav>

  <section class="relative h-screen flex items-center justify-center overflow-hidden">
    <video autoplay loop muted playsinline class="video-bg opacity-30">
      <source src="https://assets.mixkit.co/videos/preview/mixkit-futuristic-hud-scifi-interface-41761-large.mp4" type="video/mp4">
    </video>
    <div class="relative z-10 text-center px-4 max-w-5xl mx-auto">
      <h1 class="text-6xl md:text-9xl font-black tracking-tight mb-4 text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-500">{{BUSINESS_NAME}}</h1>
      <p class="text-xl text-purple-300 font-bold mb-8 tracking-widest uppercase">Next-Generation Content Distribution & Satellite Broadcasting</p>
      <a href="#contact" class="border border-purple-500 hover:bg-purple-500/20 px-8 py-3 rounded text-sm font-bold uppercase tracking-widest inline-block transition">Studio Access</a>
    </div>
  </section>

  <div class="py-20 max-w-7xl mx-auto px-6 space-y-16">
    <div class="text-center"><h2 class="text-3xl font-bold uppercase tracking-widest text-purple-400 mb-4">Transmission Mastery</h2><p class="text-slate-400 max-w-xl mx-auto">Delivering high-fidelity audio and ultra-HD video streams across global satellite constellations and digital networks.</p></div>
    <div class="grid md:grid-cols-3 gap-8">
      <div class="border border-purple-500/30 p-8 bg-purple-900/20"><i class="fa-solid fa-satellite-dish text-4xl text-purple-400 mb-4"></i><h4 class="font-bold mb-2">Uplink Facilities</h4><p class="text-xs text-slate-400">Redundant earth stations ensuring 99.999% uptime.</p></div>
      <div class="border border-purple-500/30 p-8 bg-purple-900/20"><i class="fa-solid fa-podcast text-4xl text-purple-400 mb-4"></i><h4 class="font-bold mb-2">Digital Radio</h4><p class="text-xs text-slate-400">Multi-channel audio syndication.</p></div>
      <div class="border border-purple-500/30 p-8 bg-purple-900/20"><i class="fa-solid fa-tv text-4xl text-purple-400 mb-4"></i><h4 class="font-bold mb-2">OTT Platforms</h4><p class="text-xs text-slate-400">Custom streaming infrastructure deployment.</p></div>
    </div>
    <div><h3 class="text-xl font-bold mb-2 text-purple-300">Live Event Coverage</h3><p class="text-slate-400">Multi-camera outside broadcast vans equipped with real-time encoding for instant global transmission.</p></div>
    <div><h3 class="text-xl font-bold mb-2 text-purple-300">Post Production</h3><p class="text-slate-400">Advanced color grading suites and spatial audio mixing facilities for cinematic mastering.</p></div>
    <div><h3 class="text-xl font-bold mb-2 text-purple-300">Archival Preservation</h3><p class="text-slate-400">LTO tape libraries and cloud cold storage ensuring long-term security of valuable media assets.</p></div>
    <div><h3 class="text-xl font-bold mb-2 text-purple-300">Regulatory Compliance</h3><p class="text-slate-400">Strict adherence to international broadcasting standards and content licensing agreements.</p></div>
  </div>

  <section id="contact" class="bg-black py-20 px-6 border-t border-purple-500/30 text-center">
    <h3 class="text-2xl font-bold uppercase tracking-widest text-purple-400 mb-6">Transmission Control Center</h3>
    <div class="max-w-lg mx-auto bg-purple-950 p-6 border border-purple-800 text-left space-y-4 text-sm font-sans">
      <div><strong>Studio HQ:</strong> {{ADDRESS}}</div>
      <div><strong>Control Room:</strong> {{PHONE}}</div>
      <div><strong>Network Ops:</strong> {{EMAIL}}</div>
    </div>
  </section>

  <footer class="bg-purple-950 text-slate-600 text-xs py-6 text-center">© 2026 {{BUSINESS_NAME}}. All Rights Reserved.</footer>

  <div id="loginModal" class="fixed inset-0 bg-black/80 z-50 hidden items-center justify-center p-4">
    <div class="bg-slate-900 border border-purple-500 w-full max-w-md p-6 rounded relative text-white font-sans">
      <button onclick="document.getElementById('loginModal').classList.remove('modal-active')" class="absolute top-4 right-4"><i class="fa-solid fa-xmark"></i></button>
      <h3 class="text-xl font-bold mb-4 font-mono text-purple-400">Producer Authentication</h3>
      <button class="w-full bg-white text-black font-bold py-2 rounded mb-4 flex items-center justify-center gap-2"><i class="fa-brands fa-google text-red-500"></i> Continue with Google</button>
      <form onsubmit="event.preventDefault();" class="space-y-4 font-mono">
        <input type="email" placeholder="Operator Email" class="w-full bg-slate-800 border p-2 rounded">
        <input type="password" placeholder="Keycode" class="w-full bg-slate-800 border p-2 rounded">
        <button type="submit" class="w-full bg-purple-600 font-bold py-2 rounded uppercase">Authorize</button>
      </form>
    </div>
  </div>
</body>
</html>
"""

# DIALECT/LAYOUT 5: ENTERPRISE TECHNOLOGY & SOFTWARE
TECH_HTML = """<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{BUSINESS_NAME}} | Enterprise Software Solutions</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  <style>.modal-active { display: flex !important; margin:0; } .video-bg { position: absolute; top: 50%; left: 50%; min-width: 100%; min-height: 100%; width: auto; height: auto; transform: translateX(-50%) translateY(-50%); object-fit: cover; }</style>
</head>
<body class="bg-slate-900 text-slate-100 font-sans">
  <nav class="fixed top-0 w-full z-50 bg-slate-950/80 backdrop-blur border-b border-cyan-500 p-4 flex justify-between items-center">
    <span class="text-xl font-black text-cyan-400 tracking-widest uppercase">{{BUSINESS_NAME}}</span>
    <button onclick="document.getElementById('loginModal').classList.add('modal-active')" class="bg-gradient-to-r from-cyan-500 to-blue-600 px-4 py-2 rounded font-bold text-xs">Developer Console</button>
  </nav>

  <section class="relative h-screen flex items-center justify-center overflow-hidden">
    <video autoplay loop muted playsinline class="video-bg opacity-30">
      <source src="https://assets.mixkit.co/videos/preview/mixkit-digital-animation-of-blue-connections-41662-large.mp4" type="video/mp4">
    </video>
    <div class="relative z-10 text-center px-4 max-w-4xl mx-auto">
      <h1 class="text-5xl md:text-8xl font-black tracking-tighter mb-4">{{BUSINESS_NAME}}</h1>
      <p class="text-xl text-cyan-400 mb-8 font-mono">Architecting Scalable Cloud Systems & AI Automation</p>
      <a href="#contact" class="bg-cyan-500 text-slate-950 px-8 py-3 rounded font-black text-sm uppercase tracking-widest inline-block shadow">Deploy Solution</a>
    </div>
  </section>

  <div class="py-24 max-w-7xl mx-auto px-6 space-y-20">
    <div class="tex-center"><h2 class="text-4xl font-bold tracking-tight text-white mb-4">Enterprise Architecture</h2><p class="text-slate-400">High-throughput microservices and distributed computing frameworks engineered for maximum reliability.</p></div>
    <div class="grid md:grid-cols-3 gap-6"><div class="bg-black p-8 border border-cyan-500/50 rounded"><i class="fa-solid fa-cloud-arrow-up text-3xl text-cyan-400 mb-4"></i><h4 class="font-bold mb-2">Cloud Migration</h4><p class="text-xs text-slate-400">Zero-downtime transition to multi-cloud environments.</p></div><div class="bg-black p-8 border border-cyan-500/50 rounded"><i class="fa-solid fa-robot text-3xl text-cyan-400 mb-4"></i><h4 class="font-bold mb-2">AI Integration</h4><p class="text-xs text-slate-400">Custom LLM training and automated workflow deployment.</p></div><div class="bg-black p-8 border border-cyan-500/50 rounded"><i class="fa-solid fa-shield-halved text-3xl text-cyan-400 mb-4"></i><h4 class="font-bold mb-2">Cybersecurity</h4><p class="text-xs text-slate-400">Continuous threat monitoring and penetration testing.</p></div></div>
    <div><h3 class="text-xl font-bold mb-2 text-cyan-400">Enterprise Resource Planning</h3><p class="text-slate-400">Customized ERP platforms consolidating financial, operational, and human resource management into a single pane of glass.</p></div>
    <div><h3 class="text-xl font-bold mb-2 text-cyan-400">API Gateway Management</h3><p class="text-slate-400">Secure routing and rate-limiting infrastructure handling millions of daily transactional calls with sub-millisecond latency.</p></div>
    <div><h3 class="text-xl font-bold mb-2 text-cyan-400">Data Analytics Warehouses</h3><p class="text-slate-400">Real-time telemetry ingestion pipelines enabling predictive business intelligence and automated reporting.</p></div>
    <div><h3 class="text-xl font-bold mb-2 text-cyan-400">DevOps Automation</h3><p class="text-slate-400">CI/CD pipeline optimization ensuring rapid, error-free deployment cycles across staging and production environments.</p></div>
  </div>

  <section id="contact" class="bg-black py-20 px-6 border-t border-cyan-500 text-center">
    <h3 class="text-2xl font-bold uppercase tracking-widest text-cyan-400 mb-6">Central Operations Desk</h3>
    <div class="max-w-md mx-auto bg-slate-900 p-6 border border-slate-800 text-left space-y-2 text-xs font-mono">
      <div><strong>HQ:</strong> {{ADDRESS}}</div>
      <div><strong>Toll-Free:</strong> {{PHONE}}</div>
      <div><strong>Helpdesk:</strong> {{EMAIL}}</div>
    </div>
  </section>

  <footer class="bg-slate-950 text-slate-500 text-xs py-6 text-center">© 2026 {{BUSINESS_NAME}}. All Rights Reserved.</footer>

  <div id="loginModal" class="fixed inset-0 bg-black/80 z-50 hidden items-center justify-center p-4">
    <div class="bg-slate-900 border border-cyan-500 w-full max-w-md p-6 rounded relative text-white font-mono">
      <button onclick="document.getElementById('loginModal').classList.remove('modal-active')" class="absolute top-4 right-4 text-slate-400"><i class="fa-solid fa-xmark"></i></button>
      <h3 class="text-xl font-bold mb-4 text-cyan-400">System Access</h3>
      <button class="w-full bg-white text-black font-bold py-2 rounded mb-4 flex items-center justify-center gap-2"><i class="fa-brands fa-google text-red-500"></i> Continue with Google</button>
      <form onsubmit="event.preventDefault();" class="space-y-4">
        <input type="email" placeholder="Corporate Root Email" class="w-full bg-slate-800 border p-2 rounded">
        <input type="password" placeholder="Access Token" class="w-full bg-slate-800 border p-2 rounded">
        <button type="submit" class="w-full bg-cyan-500 text-slate-950 font-bold py-2 rounded uppercase">Authenticate</button>
      </form>
    </div>
  </div>
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
            if "category" in key or "cat" in key:
                data["category"] = val.lower()
            elif "name" in key:
                data["name"] = val
            elif "email" in key or "gmail" in key:
                data["email"] = val
            elif "phone" in key or "mobile" in key or "number" in key:
                data["phone"] = val
            elif "address" in key or "location" in key:
                data["address"] = val
    return data

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "🏗️ *Multi-Category Professional Website Generator*\n\n"
        "Mujhe niche diye format me details bhejo, mai ekdum unique aur professional website file bhej dunga:\n\n"
        "Available Categories: `construction`, `travel`, `grocery`, `broadcasting`, `tech`\n\n"
        "`Category: construction`\n"
        "`Name: Shree Balaji Infra`\n"
        "`Email: contact@domain.com`\n"
        "`Phone: +91 9876543210`\n"
        "`Address: Plot 12, Ind Area, Indore, MP`\n"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    data = parse_details(message.text)
    
    if not all(k in data for k in ["category", "name", "email", "phone", "address"]):
        bot.reply_to(
            message,
            "⚠️ *Error: Saari details sahi format me bhejo!*\n\n"
            "Format:\n"
            "`Category: <category>`\n"
            "`Name: <business name>`\n"
            "`Email: <email>`\n"
            "`Phone: <phone>`\n"
            "`Address: <address>`",
            parse_mode="Markdown"
        )
        return

    cat = data["category"]
    if "construction" in cat:
        html_output = CONSTRUCTION_HTML
    elif "travel" in cat:
        html_output = TRAVEL_HTML
    elif "grocery" in cat:
        html_output = GROCERY_HTML
    elif "broadcasting" in cat:
        html_output = BROADCASTING_HTML
    elif "tech" in cat:
        html_output = TECH_HTML
    else:
        bot.reply_to(message, " Invalid category! Choose from: construction, travel, grocery, broadcasting, tech.")
        return

    html_output = html_output.replace("{{BUSINESS_NAME}}", data["name"])
    html_output = html_output.replace("{{EMAIL}}", data["email"])
    html_output = html_output.replace("{{PHONE}}", data["phone"])
    html_output = html_output.replace("{{ADDRESS}}", data["address"])

    file_bytes = io.BytesIO(html_output.encode("utf-8"))
    clean_filename = re.sub(r'[^a-zA-Z0-9]', '_', data["name"]).lower() + f"_{cat}_index.html"
    file_bytes.name = clean_filename

    caption = (
        f"✅ *Professional {cat.upper()} Website Ready!*\n\n"
        f"🏢 *Entity:* {data['name']}\n"
        f"📍 *Address:* {data['address']}\n\n"
        f"👉 Is file ko download karke Vercel par direct drop karo."
    )

    bot.send_document(chat_id=message.chat.id, document=file_bytes, caption=caption, parse_mode="Markdown")

app = Flask(__name__)
@app.route('/')
def home():
    return "Multi-Category Bot is running 24/7!"

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
