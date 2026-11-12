import os
import re
import io
import json
import threading
from flask import Flask
import telebot

BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
bot = telebot.TeleBot(BOT_TOKEN)

STATE_FILE = "template_counter.json"
state_lock = threading.Lock()

def get_next_template_index():
    """Returns 0 to 9 strictly in 1 -> 2 -> 3 ... -> 10 sequence."""
    with state_lock:
        idx = 0
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, "r") as f:
                    data = json.load(f)
                    idx = int(data.get("current_index", 0))
            except Exception:
                idx = 0
        current = idx % 10
        next_idx = (current + 1) % 10
        try:
            with open(STATE_FILE, "w") as f:
                json.dump({"current_index": next_idx}, f)
        except Exception:
            pass
        return current

def set_template_index(num_1_to_10):
    with state_lock:
        idx = (max(1, min(10, num_1_to_10)) - 1) % 10
        try:
            with open(STATE_FILE, "w") as f:
                json.dump({"current_index": idx}, f)
        except Exception:
            pass
        return idx

# ==============================================================================
# 10 DISTINCT CONSTRUCTION INTERFACES (WHITE THEME + UNIQUE VIDEOS/IMAGES/STYLES)
# ==============================================================================
TEMPLATES_DATA = [
    # 1. SAFETY ORANGE & SLATE
    {
        "id": 1,
        "theme_name": "Imperial Safety Orange & Slate",
        "font_name": "Plus Jakarta Sans",
        "font_url": "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap",
        "accent": "orange-600",
        "accent_hover": "orange-700",
        "accent_light": "orange-50",
        "accent_text": "orange-600",
        "badge_bg": "orange-100",
        "badge_text": "orange-800",
        "dark_bg": "slate-900",
        "hero_style": "split",
        "card_radius": "rounded-3xl",
        "video_url": "https://cdn.pixabay.com/video/2020/05/25/40130-424930032_large.mp4",
        "hero_img": "https://images.unsplash.com/photo-1541888946425-d09bb18086f6?auto=format&fit=crop&w=1920&q=85",
        "panorama_img": "https://images.unsplash.com/photo-1503387762-592deb58ef4e?auto=format&fit=crop&w=1920&q=85",
        "about_imgs": [
            "https://images.unsplash.com/photo-1504307651254-35680f356dfd?auto=format&fit=crop&w=1000&q=85",
            "https://images.unsplash.com/photo-1590674899484-d5640e854abe?auto=format&fit=crop&w=1000&q=85"
        ],
        "ongoing_imgs": [
            ("https://images.unsplash.com/photo-1590674899484-d5640e854abe?auto=format&fit=crop&w=1000&q=85", "Skyline Commercial Plaza", "G + 14 Floors", "72%", "RCC 10th Floor Slab Casting Active"),
            ("https://images.unsplash.com/photo-1508450859948-4e04fabaa4ea?auto=format&fit=crop&w=1000&q=85", "Emerald Heights Residency", "G + 19 Towers", "84%", "External Scaffolding & Brickwork Stage"),
            ("https://images.unsplash.com/photo-1531834685032-c34bf0d84c77?auto=format&fit=crop&w=1000&q=85", "Metro Industrial Park", "Heavy PEB & RCC", "48%", "Deep Raft Foundation & Steel Binding")
        ],
        "completed_imgs": [
            ("https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1000&q=85", "Apex Corporate Pinnacle", "1,85,000 Sq.Ft.", "Commercial Glass Facade Tower"),
            ("https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=1000&q=85", "Royal Heritage Enclave", "2,40,000 Sq.Ft.", "Luxury 160-Flat Residential Society"),
            ("https://images.unsplash.com/photo-1577495508048-b635879837f1?auto=format&fit=crop&w=1000&q=85", "Vertex Trade Center", "1,10,000 Sq.Ft.", "Turnkey Retail & Office Complex")
        ],
        "worker_imgs": [
            ("https://images.unsplash.com/photo-1504307651254-35680f356dfd?auto=format&fit=crop&w=900&q=85", "RCC & Steel Bar-Bending Crew", "220+ Active Site Masons & Carpenters"),
            ("https://images.unsplash.com/photo-1581094794329-c8112a89af12?auto=format&fit=crop&w=900&q=85", "Structural Civil Engineers", "Blueprint Execution & Cube Testing"),
            ("https://images.unsplash.com/photo-1541888946425-d09bb18086f6?auto=format&fit=crop&w=900&q=85", "High-Rise Safety Supervisors", "100% Helmet & Harness Compliance"),
            ("https://images.unsplash.com/photo-1504917599217-d4dc5ebe6122?auto=format&fit=crop&w=900&q=85", "Heavy Crane & Rigging Team", "Tower Crane & RMC Pump Operators")
        ]
    },

    # 2. ROYAL COBALT BLUE & STEEL
    {
        "id": 2,
        "theme_name": "Royal Cobalt Blue & Architectural Steel",
        "font_name": "Outfit",
        "font_url": "https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap",
        "accent": "blue-600",
        "accent_hover": "blue-700",
        "accent_light": "blue-50",
        "accent_text": "blue-600",
        "badge_bg": "blue-100",
        "badge_text": "blue-800",
        "dark_bg": "slate-950",
        "hero_style": "centered",
        "card_radius": "rounded-2xl",
        "video_url": "https://assets.mixkit.co/videos/preview/mixkit-construction-site-of-a-modern-building-41004-large.mp4",
        "hero_img": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=85",
        "panorama_img": "https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=1920&q=85",
        "about_imgs": [
            "https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=1000&q=85",
            "https://images.unsplash.com/photo-1508450859948-4e04fabaa4ea?auto=format&fit=crop&w=1000&q=85"
        ],
        "ongoing_imgs": [
            ("https://images.unsplash.com/photo-1508450859948-4e04fabaa4ea?auto=format&fit=crop&w=1000&q=85", "BlueChip IT Park Tower-B", "G + 16 Floors", "78%", "Curtain Wall & Structural Glazing"),
            ("https://images.unsplash.com/photo-1590674899484-d5640e854abe?auto=format&fit=crop&w=1000&q=85", "Sapphire Grand Apartments", "3 Towers (G+15)", "64%", "6th Floor RCC Slab & Column Pouring"),
            ("https://images.unsplash.com/photo-1578575437130-527eed3abbec?auto=format&fit=crop&w=1000&q=85", "National Logistics Hub", "Mega Warehouse", "55%", "Heavy Truss & VDF Concrete Flooring")
        ],
        "completed_imgs": [
            ("https://images.unsplash.com/photo-1554469384-e58fac16e23a?auto=format&fit=crop&w=1000&q=85", "Millennium Business Square", "2,20,000 Sq.Ft.", "Grade-A Corporate Office Building"),
            ("https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?auto=format&fit=crop&w=1000&q=85", "Crown Residency Towers", "1,95,000 Sq.Ft.", "Earthquake Resistant Luxury Flats"),
            ("https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1000&q=85", "Bespoke Commercial Villa Park", "1,30,000 Sq.Ft.", "Gated Architectural Township")
        ],
        "worker_imgs": [
            ("https://images.unsplash.com/photo-1581094794329-c8112a89af12?auto=format&fit=crop&w=900&q=85", "Senior Structural Planners", "AutoCAD & STAAD.Pro Site Team"),
            ("https://images.unsplash.com/photo-1504307651254-35680f356dfd?auto=format&fit=crop&w=900&q=85", "Master Shuttering Workforce", "Steel Formwork & Column Specialists"),
            ("https://images.unsplash.com/photo-1504917599217-d4dc5ebe6122?auto=format&fit=crop&w=900&q=85", "Welding & Fabrication Unit", "High-Tensile Structural Steel Crew"),
            ("https://images.unsplash.com/photo-1541888946425-d09bb18086f6?auto=format&fit=crop&w=900&q=85", "Quality Audit Engineers", "On-Site Ultrasonic & Slump Testing")
        ]
    },

    # 3. EMERALD GREEN & CHARCOAL
    {
        "id": 3,
        "theme_name": "Eco-Structural Emerald & Charcoal",
        "font_name": "Manrope",
        "font_url": "https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap",
        "accent": "emerald-600",
        "accent_hover": "emerald-700",
        "accent_light": "emerald-50",
        "accent_text": "emerald-600",
        "badge_bg": "emerald-100",
        "badge_text": "emerald-800",
        "dark_bg": "zinc-900",
        "hero_style": "showcase",
        "card_radius": "rounded-3xl",
        "video_url": "https://assets.mixkit.co/videos/preview/mixkit-aerial-view-of-city-buildings-on-a-sunny-day-41465-large.mp4",
        "hero_img": "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=1920&q=85",
        "panorama_img": "https://images.unsplash.com/photo-1590674899484-d5640e854abe?auto=format&fit=crop&w=1920&q=85",
        "about_imgs": [
            "https://images.unsplash.com/photo-1531834685032-c34bf0d84c77?auto=format&fit=crop&w=1000&q=85",
            "https://images.unsplash.com/photo-1504307651254-35680f356dfd?auto=format&fit=crop&w=1000&q=85"
        ],
        "ongoing_imgs": [
            ("https://images.unsplash.com/photo-1531834685032-c34bf0d84c77?auto=format&fit=crop&w=1000&q=85", "Greenfield Eco-Commercial Hub", "G + 11 Floors", "61%", "AAC Block Masonry & RCC Framing"),
            ("https://images.unsplash.com/photo-1590674899484-d5640e854abe?auto=format&fit=crop&w=1000&q=85", "Verdant Living Towers", "G + 22 Floors", "79%", "16th Floor Slab Casting Completed"),
            ("https://images.unsplash.com/photo-1508450859948-4e04fabaa4ea?auto=format&fit=crop&w=1000&q=85", "BioTech Institutional Wing", "6-Story Campus", "88%", "Exterior Plaster & Terrace Waterproofing")
        ],
        "completed_imgs": [
            ("https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=1000&q=85", "Oasis Eco-Corporate Park", "2,60,000 Sq.Ft.", "IGBC Gold Rated Commercial Building"),
            ("https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1000&q=85", "Harmony Heights Society", "1,75,000 Sq.Ft.", "Completed Multi-Story Residential Complex"),
            ("https://images.unsplash.com/photo-1577495508048-b635879837f1?auto=format&fit=crop&w=1000&q=85", "Aura Retail Boulevard", "1,20,000 Sq.Ft.", "Modern High-Street Commercial Plaza")
        ],
        "worker_imgs": [
            ("https://images.unsplash.com/photo-1504307651254-35680f356dfd?auto=format&fit=crop&w=900&q=85", "Dedicated Concrete & Curing Crew", "Round-the-Clock RCC Execution"),
            ("https://images.unsplash.com/photo-1541888946425-d09bb18086f6?auto=format&fit=crop&w=900&q=85", "Project Management Directorate", "Timeline & BOQ Billing Control"),
            ("https://images.unsplash.com/photo-1581094794329-c8112a89af12?auto=format&fit=crop&w=900&q=85", "Geotechnical & Soil Engineers", "Deep Pile Foundation Specialists"),
            ("https://images.unsplash.com/photo-1503387762-592deb58ef4e?auto=format&fit=crop&w=900&q=85", "MEP & Finishing Artisans", "Electrical, Fire-Fighting & Glazing")
        ]
    },

    # 4. CRIMSON RED & OBSIDIAN
    {
        "id": 4,
        "theme_name": "Heavy Industrial Crimson & Obsidian",
        "font_name": "Space Grotesk",
        "font_url": "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap",
        "accent": "red-600",
        "accent_hover": "red-700",
        "accent_light": "red-50",
        "accent_text": "red-600",
        "badge_bg": "red-100",
        "badge_text": "red-800",
        "dark_bg": "neutral-950",
        "hero_style": "split",
        "card_radius": "rounded-xl",
        "video_url": "https://cdn.pixabay.com/video/2020/05/25/40130-424930032_large.mp4",
        "hero_img": "https://images.unsplash.com/photo-1508450859948-4e04fabaa4ea?auto=format&fit=crop&w=1920&q=85",
        "panorama_img": "https://images.unsplash.com/photo-1541888946425-d09bb18086f6?auto=format&fit=crop&w=1920&q=85",
        "about_imgs": [
            "https://images.unsplash.com/photo-1504917599217-d4dc5ebe6122?auto=format&fit=crop&w=1000&q=85",
            "https://images.unsplash.com/photo-1590674899484-d5640e854abe?auto=format&fit=crop&w=1000&q=85"
        ],
        "ongoing_imgs": [
            ("https://images.unsplash.com/photo-1590674899484-d5640e854abe?auto=format&fit=crop&w=1000&q=85", "Redstone Commercial Center", "G + 15 Stories", "69%", "Heavy RCC Beam & Slab Shuttering"),
            ("https://images.unsplash.com/photo-1531834685032-c34bf0d84c77?auto=format&fit=crop&w=1000&q=85", "Vulcan Industrial Complex", "Heavy Factory Civil", "53%", "Plinth Beam & RCC Column Erection"),
            ("https://images.unsplash.com/photo-1508450859948-4e04fabaa4ea?auto=format&fit=crop&w=1000&q=85", "Citadel Residential Towers", "G + 20 Floors", "81%", "Brickwork & Double-Coat Plastering")
        ],
        "completed_imgs": [
            ("https://images.unsplash.com/photo-1577495508048-b635879837f1?auto=format&fit=crop&w=1000&q=85", "Titan Corporate Headquarters", "2,10,000 Sq.Ft.", "Turnkey Structural & Facade Marvel"),
            ("https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1000&q=85", "phoenix Commercial Mall", "1,65,000 Sq.Ft.", "Multi-Level Retail & Multiplex Building"),
            ("https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=1000&q=85", "scarlet Crest Apartments", "2,80,000 Sq.Ft.", "Delivered 200-Unit Housing Project")
        ],
        "worker_imgs": [
            ("https://images.unsplash.com/photo-1504917599217-d4dc5ebe6122?auto=format&fit=crop&w=900&q=85", "Heavy Steel & Rigging Crew", "Fe-550D TMT Reinforcement Experts"),
            ("https://images.unsplash.com/photo-1504307651254-35680f356dfd?auto=format&fit=crop&w=900&q=85", "On-Site Masonry Battalion", "350+ Skilled Masons & Bar-Benders"),
            ("https://images.unsplash.com/photo-1581094794329-c8112a89af12?auto=format&fit=crop&w=900&q=85", "Chief Structural Auditors", "IS-456 Seismic Code Compliance"),
            ("https://images.unsplash.com/photo-1541888946425-d09bb18086f6?auto=format&fit=crop&w=900&q=85", "Excavation & Fleet Operators", "JCB, Poclain & Batching Plant Crew")
        ]
    },

    # 5. AMBER GOLD & NAVY
    {
        "id": 5,
        "theme_name": " Sovereign Amber Gold & Deep Navy",
        "font_name": "Urbanist",
        "font_url": "https://fonts.googleapis.com/css2?family=Urbanist:wght@400;500;600;700;800&display=swap",
        "accent": "amber-600",
        "accent_hover": "amber-700",
        "accent_light": "amber-50",
        "accent_text": "amber-600",
        "badge_bg": "amber-100",
        "badge_text": "amber-900",
        "dark_bg": "slate-900",
        "hero_style": "centered",
        "card_radius": "rounded-3xl",
        "video_url": "https://assets.mixkit.co/videos/preview/mixkit-modern-city-buildings-and-skyscrapers-41551-large.mp4",
        "hero_img": "https://images.unsplash.com/photo-1503387762-592deb58ef4e?auto=format&fit=crop&w=1920&q=85",
        "panorama_img": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=85",
        "about_imgs": [
            "https://images.unsplash.com/photo-1541888946425-d09bb18086f6?auto=format&fit=crop&w=1000&q=85",
            "https://images.unsplash.com/photo-1531834685032-c34bf0d84c77?auto=format&fit=crop&w=1000&q=85"
        ],
        "ongoing_imgs": [
            ("https://images.unsplash.com/photo-1508450859948-4e04fabaa4ea?auto=format&fit=crop&w=1000&q=85", "Golden Gate Business Tower", "G + 17 Floors", "75%", "12th Floor Slab & Core Wall Active"),
            ("https://images.unsplash.com/photo-1590674899484-d5640e854abe?auto=format&fit=crop&w=1000&q=85", "Aurum Luxury Residency", "G + 14 Towers", "66%", "RCC Superstructure & Brickwork"),
            ("https://images.unsplash.com/photo-1531834685032-c34bf0d84c77?auto=format&fit=crop&w=1000&q=85", "Sovereign Institutional Block", "Hospital & Wing", "42%", "Basement Retaining Wall & Raft")
        ],
        "completed_imgs": [
            ("https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1000&q=85", "Monarch Corporate Plaza", "1,90,000 Sq.Ft.", "Completed 12-Story Commercial Hub"),
            ("https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?auto=format&fit=crop&w=1000&q=85", "Regalia Sky-Villas", "2,50,000 Sq.Ft.", "Handed-Over Premium Apartment Complex"),
            ("https://images.unsplash.com/photo-1554469384-e58fac16e23a?auto=format&fit=crop&w=1000&q=85", "Chancellor Trade Tower", "1,40,000 Sq.Ft.", "Turnkey Banking & Corporate Building")
        ],
        "worker_imgs": [
            ("https://images.unsplash.com/photo-1504307651254-35680f356dfd?auto=format&fit=crop&w=900&q=85", "Master Masons & Plaster Crew", "Precision Line-Level Execution"),
            ("https://images.unsplash.com/photo-1581094794329-c8112a89af12?auto=format&fit=crop&w=900&q=85", "Chartered Structural Engineers", "Seismic & Wind-Load Design Team"),
            ("https://images.unsplash.com/photo-1541888946425-d09bb18086f6?auto=format&fit=crop&w=900&q=85", "Site Inspection Directorate", "Daily Cube Test & Material Audit"),
            ("https://images.unsplash.com/photo-1504917599217-d4dc5ebe6122?auto=format&fit=crop&w=900&q=85", "Tower Crane & Concrete Crew", "High-Reach Boom Placer Operators")
        ]
    },

    # 6. TEAL CYAN & GRAPHITE
    {
        "id": 6,
        "theme_name": "Modernist Teal Cyan & Graphite",
        "font_name": "DM Sans",
        "font_url": "https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap",
        "accent": "teal-600",
        "accent_hover": "teal-700",
        "accent_light": "teal-50",
        "accent_text": "teal-600",
        "badge_bg": "teal-100",
        "badge_text": "teal-800",
        "dark_bg": "slate-900",
        "hero_style": "showcase",
        "card_radius": "rounded-2xl",
        "video_url": "https://assets.mixkit.co/videos/preview/mixkit-construction-site-of-a-modern-building-41004-large.mp4",
        "hero_img": "https://images.unsplash.com/photo-1577495508048-b635879837f1?auto=format&fit=crop&w=1920&q=85",
        "panorama_img": "https://images.unsplash.com/photo-1504307651254-35680f356dfd?auto=format&fit=crop&w=1920&q=85",
        "about_imgs": [
            "https://images.unsplash.com/photo-1590674899484-d5640e854abe?auto=format&fit=crop&w=1000&q=85",
            "https://images.unsplash.com/photo-1581094794329-c8112a89af12?auto=format&fit=crop&w=1000&q=85"
        ],
        "ongoing_imgs": [
            ("https://images.unsplash.com/photo-1590674899484-d5640e854abe?auto=format&fit=crop&w=1000&q=85", "Axis Cyber-Commercial Park", "G + 13 Floors", "74%", "9th Floor Slab & Shuttering Active"),
            ("https://images.unsplash.com/photo-1508450859948-4e04fabaa4ea?auto=format&fit=crop&w=1000&q=85", "Marina Bay Residency", "G + 21 Towers", "86%", "External Elevation & Glazing Work"),
            ("https://images.unsplash.com/photo-1531834685032-c34bf0d84c77?auto=format&fit=crop&w=1000&q=85", "Zenith Cold-Chain & Logistics", "Industrial Civil", "51%", "Heavy RCC Columns & Dock Levelers")
        ],
        "completed_imgs": [
            ("https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=1000&q=85", "pacifica Corporate Towers", "2,05,000 Sq.Ft.", "Completed Twin Commercial Buildings"),
            ("https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1000&q=85", "solitaire Business Hub", "1,55,000 Sq.Ft.", "Occupied IT & Financial Center"),
            ("https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1000&q=85", "Turquoise Park Villas", "1,80,000 Sq.Ft.", "Turnkey Luxury Residential Enclave")
        ],
        "worker_imgs": [
            ("https://images.unsplash.com/photo-1504307651254-35680f356dfd?auto=format&fit=crop&w=900&q=85", "High-Rise Shuttering Force", "Modular Mivan & Plywood Formwork"),
            ("https://images.unsplash.com/photo-1541888946425-d09bb18086f6?auto=format&fit=crop&w=900&q=85", "Civil Surveying Engineers", "Total Station & Laser Leveling"),
            ("https://images.unsplash.com/photo-1581094794329-c8112a89af12?auto=format&fit=crop&w=900&q=85", "RMC Concrete Technologists", "M30/M40 Grade Mix Design Control"),
            ("https://images.unsplash.com/photo-1503387762-592deb58ef4e?auto=format&fit=crop&w=900&q=85", "Facade & Waterproofing Crew", "ACP Cladding & Chemical Coating")
        ]
    },

    # 7. INDIGO PURPLE & DARK SLATE
    {
        "id": 7,
        "theme_name": "Executive Indigo & Structural Slate",
        "font_name": "Lexend",
        "font_url": "https://fonts.googleapis.com/css2?family=Lexend:wght@400;500;600;700;800&display=swap",
        "accent": "indigo-600",
        "accent_hover": "indigo-700",
        "accent_light": "indigo-50",
        "accent_text": "indigo-600",
        "badge_bg": "indigo-100",
        "badge_text": "indigo-800",
        "dark_bg": "slate-950",
        "hero_style": "split",
        "card_radius": "rounded-3xl",
        "video_url": "https://cdn.pixabay.com/video/2020/05/25/40130-424930032_large.mp4",
        "hero_img": "https://images.unsplash.com/photo-1554469384-e58fac16e23a?auto=format&fit=crop&w=1920&q=85",
        "panorama_img": "https://images.unsplash.com/photo-1508450859948-4e04fabaa4ea?auto=format&fit=crop&w=1920&q=85",
        "about_imgs": [
            "https://images.unsplash.com/photo-1504307651254-35680f356dfd?auto=format&fit=crop&w=1000&q=85",
            "https://images.unsplash.com/photo-1541888946425-d09bb18086f6?auto=format&fit=crop&w=1000&q=85"
        ],
        "ongoing_imgs": [
            ("https://images.unsplash.com/photo-1531834685032-c34bf0d84c77?auto=format&fit=crop&w=1000&q=85", "Astra Corporate Center", "G + 16 Stories", "63%", "RCC Shear Wall & Slab Casting"),
            ("https://images.unsplash.com/photo-1590674899484-d5640e854abe?auto=format&fit=crop&w=1000&q=85", "Indigo Crest Apartments", "G + 18 Floors", "77%", "Internal Brickwork & Conduit Piping"),
            ("https://images.unsplash.com/photo-1508450859948-4e04fabaa4ea?auto=format&fit=crop&w=1000&q=85", "Vanguard Medical College Wing", "Institutional Block", "89%", "Flooring, Plaster & Finishing Stage")
        ],
        "completed_imgs": [
            ("https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1000&q=85", "Nexus Global Tower", "2,35,000 Sq.Ft.", "Landmark 16-Floor Commercial Building"),
            ("https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=1000&q=85", "Celestia Residency", "1,90,000 Sq.Ft.", "Completed High-Rise Housing Society"),
            ("https://images.unsplash.com/photo-1577495508048-b635879837f1?auto=format&fit=crop&w=1000&q=85", "Orion Retail Mall", "1,50,000 Sq.Ft.", "Handed-Over Commercial & Shopping Hub")
        ],
        "worker_imgs": [
            ("https://images.unsplash.com/photo-1581094794329-c8112a89af12?auto=format&fit=crop&w=900&q=85", "Principal Structural Engineers", "High-Rise Load & Foundation Design"),
            ("https://images.unsplash.com/photo-1504307651254-35680f356dfd?auto=format&fit=crop&w=900&q=85", "RCC & Bar-Bending Workforce", "280+ Active Certified Site Workers"),
            ("https://images.unsplash.com/photo-1504917599217-d4dc5ebe6122?auto=format&fit=crop&w=900&q=85", "Heavy Machinery Operators", "Excavators, Transit Mixers & Cranes"),
            ("https://images.unsplash.com/photo-1541888946425-d09bb18086f6?auto=format&fit=crop&w=900&q=85", "EHS Safety Supervision Team", "Strict Zero-Incident Site Protocols")
        ]
    },

    # 8. BRONZE COPPER & ZINC
    {
        "id": 8,
        "theme_name": "Architectural Terracotta Bronze & Zinc",
        "font_name": "Montserrat",
        "font_url": "https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&display=swap",
        "accent": "orange-700",
        "accent_hover": "orange-800",
        "accent_light": "orange-50",
        "accent_text": "orange-700",
        "badge_bg": "orange-100",
        "badge_text": "orange-900",
        "dark_bg": "zinc-900",
        "hero_style": "centered",
        "card_radius": "rounded-xl",
        "video_url": "https://assets.mixkit.co/videos/preview/mixkit-aerial-view-of-city-buildings-on-a-sunny-day-41465-large.mp4",
        "hero_img": "https://images.unsplash.com/photo-1531834685032-c34bf0d84c77?auto=format&fit=crop&w=1920&q=85",
        "panorama_img": "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=1920&q=85",
        "about_imgs": [
            "https://images.unsplash.com/photo-1508450859948-4e04fabaa4ea?auto=format&fit=crop&w=1000&q=85",
            "https://images.unsplash.com/photo-1504917599217-d4dc5ebe6122?auto=format&fit=crop&w=1000&q=85"
        ],
        "ongoing_imgs": [
            ("https://images.unsplash.com/photo-1590674899484-d5640e854abe?auto=format&fit=crop&w=1000&q=85", "Terracotta Business Square", "G + 14 Floors", "71%", "11th Floor Shuttering & Steel Tying"),
            ("https://images.unsplash.com/photo-1508450859948-4e04fabaa4ea?auto=format&fit=crop&w=1000&q=85", "Bronze Oak Apartments", "G + 16 Towers", "83%", "Exterior Plaster & Balcony Railing"),
            ("https://images.unsplash.com/photo-1531834685032-c34bf0d84c77?auto=format&fit=crop&w=1000&q=85", "Magnum Industrial Park", "Turnkey Factory", "49%", "Sub-Structure & Plinth Beam Ready")
        ],
        "completed_imgs": [
            ("https://images.unsplash.com/photo-1577495508048-b635879837f1?auto=format&fit=crop&w=1000&q=85", "Copperfield Corporate Hub", "1,70,000 Sq.Ft.", "Delivered Commercial Office Building"),
            ("https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?auto=format&fit=crop&w=1000&q=85", "Sunstone Grand Residency", "2,25,000 Sq.Ft.", "Occupied 140-Unit Residential Towers"),
            ("https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1000&q=85", "Zenith Financial Arcade", "1,35,000 Sq.Ft.", "Earthquake-Safe RCC Framed Plaza")
        ],
        "worker_imgs": [
            ("https://images.unsplash.com/photo-1504307651254-35680f356dfd?auto=format&fit=crop&w=900&q=85", "Brickwork & Masonry Specialists", "High-Precision Block & Plaster Team"),
            ("https://images.unsplash.com/photo-1541888946425-d09bb18086f6?auto=format&fit=crop&w=900&q=85", "Senior Civil Site Engineers", "Structural Drawing & Level Control"),
            ("https://images.unsplash.com/photo-1504917599217-d4dc5ebe6122?auto=format&fit=crop&w=900&q=85", "Steel Fabrication & Bar Crew", "Heavy Column & Beam Cage Binding"),
            ("https://images.unsplash.com/photo-1581094794329-c8112a89af12?auto=format&fit=crop&w=900&q=85", "Quality & Material Testing Lab", "Cube Strength & Rebar Tensile Checks")
        ]
    },

    # 9. SKY BLUE & MIDNIGHT
    {
        "id": 9,
        "theme_name": "Skyline Azure & Midnight Steel",
        "font_name": "Inter",
        "font_url": "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap",
        "accent": "sky-600",
        "accent_hover": "sky-700",
        "accent_light": "sky-50",
        "accent_text": "sky-600",
        "badge_bg": "sky-100",
        "badge_text": "sky-900",
        "dark_bg": "slate-950",
        "hero_style": "showcase",
        "card_radius": "rounded-3xl",
        "video_url": "https://assets.mixkit.co/videos/preview/mixkit-modern-city-buildings-and-skyscrapers-41551-large.mp4",
        "hero_img": "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?auto=format&fit=crop&w=1920&q=85",
        "panorama_img": "https://images.unsplash.com/photo-1531834685032-c34bf0d84c77?auto=format&fit=crop&w=1920&q=85",
        "about_imgs": [
            "https://images.unsplash.com/photo-1541888946425-d09bb18086f6?auto=format&fit=crop&w=1000&q=85",
            "https://images.unsplash.com/photo-1504307651254-35680f356dfd?auto=format&fit=crop&w=1000&q=85"
        ],
        "ongoing_imgs": [
            ("https://images.unsplash.com/photo-1508450859948-4e04fabaa4ea?auto=format&fit=crop&w=1000&q=85", "Azure Sky Corporate Tower", "G + 20 Floors", "76%", "15th Floor RCC Slab & Core Active"),
            ("https://images.unsplash.com/photo-1590674899484-d5640e854abe?auto=format&fit=crop&w=1000&q=85", "CloudNine Residential Park", "4 Towers (G+16)", "67%", "Superstructure & Masonry In Progress"),
            ("https://images.unsplash.com/photo-1531834685032-c34bf0d84c77?auto=format&fit=crop&w=1000&q=85", "AeroSpace Logistics Terminal", "PEB & Civil Hub", "58%", "Heavy Floor Slab & Truss Erection")
        ],
        "completed_imgs": [
            ("https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1000&q=85", "Horizon Glass Commercial Tower", "2,45,000 Sq.Ft.", "Completed 18-Story Corporate Building"),
            ("https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=1000&q=85", "BlueWaters Luxury Apartments", "2,15,000 Sq.Ft.", "Handed-Over Residential Township"),
            ("https://images.unsplash.com/photo-1554469384-e58fac16e23a?auto=format&fit=crop&w=1000&q=85", "Starlight Retail & Office Hub", "1,60,000 Sq.Ft.", "Turnkey Commercial Plaza")
        ],
        "worker_imgs": [
            ("https://images.unsplash.com/photo-1504307651254-35680f356dfd?auto=format&fit=crop&w=900&q=85", "On-Site RCC & Shuttering Crew", "300+ Active Skilled Construction Workers"),
            ("https://images.unsplash.com/photo-1581094794329-c8112a89af12?auto=format&fit=crop&w=900&q=85", "Structural Design & QA Team", "100% IS-Code Compliant Execution"),
            ("https://images.unsplash.com/photo-1541888946425-d09bb18086f6?auto=format&fit=crop&w=900&q=85", "Safety & Scaffolding Officers", "Multi-Story High-Rise Safety Gear"),
            ("https://images.unsplash.com/photo-1503387762-592deb58ef4e?auto=format&fit=crop&w=900&q=85", "Glazing & Interior Finishers", "Structural Glass, Tile & MEP Crew")
        ]
    },

    # 10. VERMILION ROSE & TITANIUM
    {
        "id": 10,
        "theme_name": "Titanium & Vermilion Heavy Civil",
        "font_name": "Syne",
        "font_url": "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap",
        "accent": "rose-600",
        "accent_hover": "rose-700",
        "accent_light": "rose-50",
        "accent_text": "rose-600",
        "badge_bg": "rose-100",
        "badge_text": "rose-900",
        "dark_bg": "zinc-950",
        "hero_style": "split",
        "card_radius": "rounded-2xl",
        "video_url": "https://cdn.pixabay.com/video/2020/05/25/40130-424930032_large.mp4",
        "hero_img": "https://images.unsplash.com/photo-1590674899484-d5640e854abe?auto=format&fit=crop&w=1920&q=85",
        "panorama_img": "https://images.unsplash.com/photo-1504307651254-35680f356dfd?auto=format&fit=crop&w=1920&q=85",
        "about_imgs": [
            "https://images.unsplash.com/photo-1531834685032-c34bf0d84c77?auto=format&fit=crop&w=1000&q=85",
            "https://images.unsplash.com/photo-1581094794329-c8112a89af12?auto=format&fit=crop&w=1000&q=85"
        ],
        "ongoing_imgs": [
            ("https://images.unsplash.com/photo-1590674899484-d5640e854abe?auto=format&fit=crop&w=1000&q=85", "Titanium Corporate Galleria", "G + 15 Floors", "80%", "13th Floor Slab & Brickwork Active"),
            ("https://images.unsplash.com/photo-1508450859948-4e04fabaa4ea?auto=format&fit=crop&w=1000&q=85", "Prime Meridian Towers", "G + 21 Stories", "73%", "RCC Superstructure & Lift Core"),
            ("https://images.unsplash.com/photo-1531834685032-c34bf0d84c77?auto=format&fit=crop&w=1000&q=85", "Apex Heavy Engineering Hub", "Industrial Plant", "52%", "Deep Pile Cap & Plinth Beam Stage")
        ],
        "completed_imgs": [
            ("https://images.unsplash.com/photo-1577495508048-b635879837f1?auto=format&fit=crop&w=1000&q=85", "Vanguard Business Pinnacle", "2,30,000 Sq.Ft.", "Handed-Over Commercial High-Rise"),
            ("https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=1000&q=85", "Imperial Grandeur Flats", "2,75,000 Sq.Ft.", "Completed 180-Unit Luxury Society"),
            ("https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1000&q=85", "Dominion Trade Tower", "1,65,000 Sq.Ft.", "Turnkey Glass & Concrete Complex")
        ],
        "worker_imgs": [
            ("https://images.unsplash.com/photo-1504307651254-35680f356dfd?auto=format&fit=crop&w=900&q=85", "Civil Masonry & Concrete Force", "250+ Skilled Site Workers & Foremen"),
            ("https://images.unsplash.com/photo-1541888946425-d09bb18086f6?auto=format&fit=crop&w=900&q=85", "Chief Structural Consultants", "Seismic Zone-IV Compliant Framing"),
            ("https://images.unsplash.com/photo-1504917599217-d4dc5ebe6122?auto=format&fit=crop&w=900&q=85", "Rigging & Crane Operations", "Heavy Lift & RMC Pumping Unit"),
            ("https://images.unsplash.com/photo-1581094794329-c8112a89af12?auto=format&fit=crop&w=900&q=85", "Site Quality & Audit Desk", "Laser Leveling & Cube Compression Lab")
        ]
    }
]


def build_hero_section(t, name, phone, email, address):
    """Generates 3 structurally distinct Hero layouts across the 10 templates."""
    ac = t["accent"]
    ach = t["accent_hover"]
    rad = t["card_radius"]

    if t["hero_style"] == "centered":
        return f"""
  <!-- HERO VARIANT B: MONUMENTAL CENTERED CINEMA HERO -->
  <section class="relative min-h-[92vh] flex items-center justify-center overflow-hidden bg-{t['dark_bg']}">
    <div class="absolute inset-0 z-0">
      <img src="{t['hero_img']}" alt="Construction" class="w-full h-full object-cover animate-live-bg opacity-45">
      <video autoplay loop muted playsinline class="absolute inset-0 w-full h-full object-cover opacity-65">
        <source src="{t['video_url']}" type="video/mp4">
      </video>
    </div>
    <div class="absolute inset-0 bg-gradient-to-b from-black/80 via-black/65 to-black/90 z-10"></div>

    <div class="relative z-20 max-w-6xl mx-auto px-6 py-24 text-center text-white">
      <div class="inline-flex items-center gap-2.5 bg-{ac} text-white px-5 py-2 rounded-full text-xs font-extrabold uppercase tracking-widest mb-8 shadow-xl">
        <span class="w-2.5 h-2.5 rounded-full bg-white animate-ping"></span>
        <span>ISO 9001:2015 Certified Civil & Building Contractors</span>
      </div>
      <h1 class="text-5xl sm:text-7xl lg:text-8xl font-black tracking-tight uppercase leading-none mb-6 drop-shadow-lg">
        {name}
      </h1>
      <div class="text-xl sm:text-3xl font-bold text-gray-200 mb-6 min-h-[42px]">
        <span class="text-{ac} bg-white px-3 py-1 rounded mr-2">LIVE:</span>
        <span id="typewriter" class="typing-cursor text-white"></span>
      </div>
      <p class="text-base sm:text-xl text-gray-300 max-w-3xl mx-auto mb-10 leading-relaxed">
        Executing landmark commercial towers, residential apartment complexes, and heavy RCC framed structures with 450+ active site workers, engineers, and modern machinery at <strong>{address}</strong>.
      </p>
      <div class="flex flex-wrap justify-center gap-5">
        <a href="#ongoing" class="bg-{ac} hover:bg-{ach} text-white font-extrabold px-10 py-5 {rad} text-base shadow-2xl transition transform hover:-translate-y-1">
          <i class="fa-solid fa-helmet-safety mr-2"></i> Explore Live Construction Sites
        </a>
        <button onclick="openModal('signupModal')" class="bg-white hover:bg-gray-100 text-slate-950 font-extrabold px-10 py-5 {rad} text-base shadow-2xl transition transform hover:-translate-y-1">
          <i class="fa-solid fa-file-signature mr-2 text-{ac}"></i> Request BOQ & Quote
        </button>
      </div>
    </div>
  </section>"""

    elif t["hero_style"] == "showcase":
        return f"""
  <!-- HERO VARIANT C: ARCHITECTURAL DUAL-FRAME LIVE VIDEO HERO -->
  <section class="relative min-h-[92vh] flex items-center overflow-hidden bg-{t['dark_bg']} py-20 px-6">
    <div class="absolute inset-0 z-0">
      <img src="{t['hero_img']}" alt="Building Site" class="w-full h-full object-cover animate-live-bg opacity-35">
      <video autoplay loop muted playsinline class="absolute inset-0 w-full h-full object-cover opacity-55">
        <source src="{t['video_url']}" type="video/mp4">
      </video>
    </div>
    <div class="absolute inset-0 bg-gradient-to-r from-black/90 via-black/75 to-black/50 z-10"></div>

    <div class="relative z-20 max-w-7xl mx-auto grid lg:grid-cols-12 gap-12 items-center w-full">
      <div class="lg:col-span-7 text-white">
        <span class="inline-block bg-{ac} text-white text-xs font-black uppercase tracking-widest px-4 py-2 rounded-lg mb-6">
          A-Grade Licensed Building Contractors
        </span>
        <h1 class="text-4xl sm:text-6xl lg:text-7xl font-black uppercase tracking-tight leading-none mb-6">
          {name}
        </h1>
        <div class="text-xl sm:text-2xl font-bold text-gray-200 mb-6">
          <span>Specialists In: </span>
          <span id="typewriter" class="text-white underline decoration-{ac} typing-cursor"></span>
        </div>
        <p class="text-base sm:text-lg text-gray-300 mb-8 leading-relaxed">
          Complete turnkey civil construction from soil testing and deep raft excavation to multi-story RCC slab casting and luxury elevation finishing.
        </p>
        <div class="flex flex-wrap gap-4">
          <a href="#completed" class="bg-{ac} hover:bg-{ach} text-white font-extrabold px-8 py-4 {rad} shadow-xl transition">
            <i class="fa-solid fa-building-circle-check mr-2"></i> Completed Buildings
          </a>
          <a href="#workforce" class="bg-white text-slate-900 hover:bg-gray-100 font-extrabold px-8 py-4 {rad} shadow-xl transition">
            <i class="fa-solid fa-users-gear mr-2 text-{ac}"></i> View Site Workforce
          </a>
        </div>
      </div>

      <div class="lg:col-span-5">
        <div class="bg-white p-3 {rad} shadow-2xl">
          <div class="relative h-[420px] overflow-hidden {rad}">
            <img src="{t['ongoing_imgs'][0][0]}" alt="Active Construction" class="w-full h-full object-cover animate-live-bg">
            <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent flex flex-col justify-end p-6 text-white">
              <span class="bg-{ac} text-white text-xs font-extrabold uppercase px-3 py-1 rounded w-max mb-2">Live Active Site</span>
              <h3 class="text-2xl font-black">{name} — Wing A</h3>
              <p class="text-xs text-gray-200 mt-1">RCC Superstructure & Tower Crane Operations Active • {phone}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>"""

    else:
        return f"""
  <!-- HERO VARIANT A: SPLIT INDUSTRIAL HERO + INSTANT ESTIMATE TERMINAL -->
  <section class="relative min-h-[92vh] flex items-center justify-center overflow-hidden bg-{t['dark_bg']}">
    <div class="absolute inset-0 z-0">
      <img src="{t['hero_img']}" alt="Construction Site" class="w-full h-full object-cover animate-live-bg opacity-45">
      <video autoplay loop muted playsinline class="absolute inset-0 w-full h-full object-cover opacity-65">
        <source src="{t['video_url']}" type="video/mp4">
      </video>
    </div>
    <div class="absolute inset-0 bg-gradient-to-r from-black/90 via-black/75 to-black/40 z-10"></div>

    <div class="relative z-20 max-w-7xl mx-auto px-6 py-20 grid lg:grid-cols-12 gap-12 items-center w-full">
      <div class="lg:col-span-8 text-white">
        <div class="inline-flex items-center gap-2 bg-{ac} text-white px-4 py-1.5 rounded-full text-xs font-extrabold uppercase tracking-wider mb-6 shadow-lg">
          <span class="w-2 h-2 rounded-full bg-white animate-ping"></span>
          <span>Turnkey Building Construction & Civil Engineering</span>
        </div>
        <h1 class="text-4xl sm:text-6xl lg:text-7xl font-black tracking-tight leading-none mb-6 uppercase">
          {name}
        </h1>
        <div class="text-xl sm:text-2xl md:text-3xl font-bold text-gray-200 mb-6 min-h-[40px]">
          <span>We Construct: </span>
          <span id="typewriter" class="text-white typing-cursor"></span>
        </div>
        <p class="text-base md:text-lg text-gray-200 max-w-2xl mb-10 leading-relaxed">
          From deep foundation excavation and Fe-550D RCC structural framing to complete architectural finishing. We construct high-strength residential apartments, commercial complexes, and industrial buildings across India.
        </p>
        <div class="flex flex-wrap gap-4">
          <a href="#ongoing" class="bg-{ac} hover:bg-{ach} text-white font-extrabold px-8 py-4 {rad} shadow-xl transition transform hover:-translate-y-1 flex items-center">
            <i class="fa-solid fa-helmet-safety mr-2.5 text-lg"></i> View Under-Construction Sites
          </a>
          <a href="#contact" class="bg-white hover:bg-gray-100 text-slate-900 font-extrabold px-8 py-4 {rad} shadow-xl transition transform hover:-translate-y-1 flex items-center">
            <i class="fa-solid fa-phone-volume mr-2.5 text-{ac}"></i> {phone}
          </a>
        </div>
      </div>

      <div class="lg:col-span-4 bg-white text-slate-900 p-8 {rad} shadow-2xl border-t-8 border-{ac}">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-xl font-extrabold">Free Construction Quote</h3>
          <span class="bg-{t['badge_bg']} text-{t['badge_text']} text-xs font-bold px-2.5 py-1 rounded">BOQ Desk</span>
        </div>
        <p class="text-xs text-slate-500 mb-6">Get an instant structural cost estimate for your residential or commercial building plot.</p>
        <form onsubmit="event.preventDefault(); alert('Thank you! Senior Engineer from {name} will contact you shortly.');" class="space-y-4 text-sm">
          <div>
            <label class="block text-xs font-bold uppercase text-slate-700 mb-1">Your Name / Company</label>
            <input type="text" required placeholder="Enter full name" class="w-full bg-gray-50 border border-gray-300 rounded-xl px-4 py-3 focus:outline-none">
          </div>
          <div>
            <label class="block text-xs font-bold uppercase text-slate-700 mb-1">Mobile Number</label>
            <input type="tel" required placeholder="+91 XXXXX XXXXX" class="w-full bg-gray-50 border border-gray-300 rounded-xl px-4 py-3 focus:outline-none">
          </div>
          <div>
            <label class="block text-xs font-bold uppercase text-slate-700 mb-1">Plot Area / Project Type</label>
            <select class="w-full bg-gray-50 border border-gray-300 rounded-xl px-4 py-3 font-semibold">
              <option>Commercial Complex / Plaza</option>
              <option>Multi-Story Residential Building</option>
              <option>RCC Structure (With Material)</option>
              <option>Industrial Shed / Warehouse</option>
            </select>
          </div>
          <button type="submit" class="w-full bg-{ac} hover:bg-{ach} text-white font-extrabold py-4 rounded-xl transition shadow-lg">
            Get Turnkey Rate Card
          </button>
        </form>
      </div>
    </div>
  </section>"""


def generate_html_for_template(t, name, phone, email, address):
    ac = t["accent"]
    ach = t["accent_hover"]
    acl = t["accent_light"]
    act = t["accent_text"]
    bbg = t["badge_bg"]
    btxt = t["badge_text"]
    dbg = t["dark_bg"]
    rad = t["card_radius"]

    hero_html = build_hero_section(t, name, phone, email, address)

    # Ongoing cards (EXTRA LARGE h-[420px] IMAGES)
    ongoing_cards = ""
    for img_url, proj_title, floors_tag, pct, desc in t["ongoing_imgs"]:
        ongoing_cards += f"""
        <div class="bg-white {rad} overflow-hidden border border-gray-200 shadow-xl hover-lift">
          <div class="relative h-[420px] overflow-hidden">
            <img src="{img_url}" alt="{proj_title}" class="w-full h-full object-cover group-hover:scale-105 transition duration-700">
            <div class="absolute inset-0 bg-gradient-to-t from-black/75 via-transparent to-black/20"></div>
            <span class="absolute top-5 left-5 bg-amber-400 text-slate-950 text-xs font-black uppercase px-4 py-1.5 rounded-full shadow-lg">
              <i class="fa-solid fa-spinner fa-spin mr-1.5"></i> Under Construction
            </span>
            <span class="absolute top-5 right-5 bg-white/95 text-slate-900 text-xs font-extrabold px-3.5 py-1.5 rounded-lg shadow">
              {floors_tag}
            </span>
            <div class="absolute bottom-5 left-5 right-5 text-white">
              <h3 class="text-2xl font-black leading-tight">{proj_title}</h3>
              <p class="text-xs text-gray-200 mt-1">{desc}</p>
            </div>
          </div>
          <div class="p-7">
            <div class="mb-2.5 flex justify-between items-center text-sm font-extrabold">
              <span class="text-slate-700">Site Structural Completion</span>
              <span class="text-{act} text-base">{pct} Done</span>
            </div>
            <div class="w-full bg-gray-200 h-3.5 rounded-full overflow-hidden">
              <div class="bg-{ac} h-full rounded-full" style="width: {pct}"></div>
            </div>
            <div class="mt-5 pt-4 border-t border-gray-100 flex justify-between text-xs font-bold text-slate-500">
              <span><i class="fa-solid fa-helmet-safety text-{act} mr-1"></i> Active Shifts</span>
              <span><i class="fa-solid fa-check-double text-emerald-600 mr-1"></i> IS-456 RCC Verified</span>
            </div>
          </div>
        </div>"""

    # Completed cards (EXTRA LARGE h-[450px] IMAGES)
    completed_cards = ""
    for img_url, proj_title, area_sqft, subtitle in t["completed_imgs"]:
        completed_cards += f"""
        <div class="bg-white {rad} overflow-hidden border border-gray-200 shadow-xl hover-lift group">
          <div class="relative h-[450px] overflow-hidden">
            <img src="{img_url}" alt="{proj_title}" class="w-full h-full object-cover group-hover:scale-110 transition duration-700">
            <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/15 to-transparent"></div>
            <span class="absolute top-5 left-5 bg-emerald-600 text-white text-xs font-black uppercase px-4 py-1.5 rounded-full shadow-lg">
              <i class="fa-solid fa-circle-check mr-1.5"></i> 100% Completed Building
            </span>
            <div class="absolute bottom-6 left-6 right-6 text-white">
              <span class="text-xs font-extrabold uppercase tracking-widest text-emerald-300 block mb-1">{subtitle}</span>
              <h3 class="text-2xl sm:text-3xl font-black">{proj_title}</h3>
            </div>
          </div>
          <div class="p-6 bg-white flex justify-between items-center text-xs font-extrabold text-slate-700">
            <span class="flex items-center"><i class="fa-solid fa-ruler-combined text-{act} text-base mr-2"></i> Built-up: {area_sqft}</span>
            <span class="bg-emerald-50 text-emerald-700 px-3 py-1 rounded-full">Handed Over</span>
          </div>
        </div>"""

    # Workforce cards (EXTRA LARGE h-[390px] IMAGES)
    worker_cards = ""
    for img_url, role_title, role_desc in t["worker_imgs"]:
        worker_cards += f"""
        <div class="bg-white text-slate-900 {rad} overflow-hidden shadow-xl border border-gray-200 hover-lift group">
          <div class="relative h-[390px] overflow-hidden">
            <img src="{img_url}" alt="{role_title}" class="w-full h-full object-cover group-hover:scale-105 transition duration-500">
            <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent"></div>
            <div class="absolute bottom-5 left-5 right-5 text-white">
              <span class="bg-{ac} text-white text-[10px] font-black uppercase px-2.5 py-1 rounded">Verified Site Crew</span>
              <h4 class="font-black text-xl mt-2">{role_title}</h4>
              <p class="text-xs text-gray-200 mt-1">{role_desc}</p>
            </div>
          </div>
        </div>"""

    return f"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{name} | Building Construction & Civil Infrastructure</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  <link rel="stylesheet" href="{t['font_url']}">
  <style>
    body {{ font-family: '{t['font_name']}', sans-serif; }}
    .modal-active {{ display: flex !important; }}
    @keyframes slowZoom {{
      0% {{ transform: scale(1); }}
      50% {{ transform: scale(1.12); }}
      100% {{ transform: scale(1); }}
    }}
    .animate-live-bg {{ animation: slowZoom 20s infinite ease-in-out; }}
    .hover-lift {{ transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1); }}
    .hover-lift:hover {{ transform: translateY(-8px); }}
    .typing-cursor::after {{ content: '|'; animation: blink 1s infinite; }}
    @keyframes blink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0; }} }}
  </style>
</head>
<body class="bg-white text-slate-900 antialiased selection:bg-{ac} selection:text-white">

  <!-- 1. TOP CORPORATE BAR -->
  <div class="bg-{dbg} text-slate-200 text-xs py-3 px-6 border-b border-slate-800">
    <div class="max-w-7xl mx-auto flex flex-wrap justify-between items-center gap-3">
      <div class="flex flex-wrap items-center gap-6">
        <a href="tel:{phone}" class="hover:text-white font-bold flex items-center">
          <i class="fa-solid fa-phone-volume text-{act} mr-2"></i> {phone}
        </a>
        <a href="mailto:{email}" class="hover:text-white font-bold flex items-center">
          <i class="fa-solid fa-envelope text-{act} mr-2"></i> {email}
        </a>
        <span class="hidden lg:flex items-center text-slate-300">
          <i class="fa-solid fa-location-dot text-{act} mr-2"></i> {address}
        </span>
      </div>
      <div class="flex items-center space-x-4">
        <span class="text-emerald-400 font-bold hidden sm:inline">
          <i class="fa-solid fa-shield-halved mr-1"></i> Govt. Registered Civil Contractor
        </span>
        <button onclick="openModal('loginModal')" class="bg-slate-800 hover:bg-slate-700 text-white px-3.5 py-1.5 rounded font-bold transition">Login</button>
        <button onclick="openModal('signupModal')" class="bg-{ac} hover:bg-{ach} text-white px-3.5 py-1.5 rounded font-bold transition">Sign Up</button>
      </div>
    </div>
  </div>

  <!-- 2. STICKY WHITE NAVIGATION -->
  <header class="bg-white/95 backdrop-blur-md sticky top-0 z-40 border-b border-gray-200 shadow-sm">
    <div class="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
      <a href="#" class="flex items-center space-x-3.5">
        <div class="w-12 h-12 {rad} bg-{ac} flex items-center justify-center text-white text-2xl shadow-lg">
          <i class="fa-solid fa-city"></i>
        </div>
        <div>
          <span class="text-xl md:text-2xl font-black tracking-tight text-slate-900 block leading-none">{name}</span>
          <span class="text-[11px] font-extrabold uppercase tracking-widest text-{act}">Building Construction & Civil Works</span>
        </div>
      </a>

      <nav class="hidden xl:flex items-center space-x-8 text-sm font-extrabold text-slate-700">
        <a href="#about" class="hover:text-{act} transition">About Company</a>
        <a href="#ongoing" class="hover:text-{act} transition">Adhuri / Ongoing Sites</a>
        <a href="#completed" class="hover:text-{act} transition">Completed Buildings</a>
        <a href="#workforce" class="hover:text-{act} transition">Site Workers</a>
        <a href="#machinery" class="hover:text-{act} transition">Machinery</a>
        <a href="#contact" class="hover:text-{act} transition">Contact Office</a>
      </nav>

      <div class="flex items-center space-x-3">
        <button onclick="openModal('loginModal')" class="hidden sm:inline-flex items-center px-5 py-2.5 border-2 border-slate-900 text-slate-900 hover:bg-slate-900 hover:text-white rounded-xl text-xs font-extrabold uppercase transition">
          Log In
        </button>
        <button onclick="openModal('signupModal')" class="inline-flex items-center px-5 py-2.5 bg-{ac} hover:bg-{ach} text-white rounded-xl text-xs font-extrabold uppercase shadow-lg transition">
          Sign Up
        </button>
      </div>
    </div>
  </header>

  {hero_html}

  <!-- 4. STATS BAR -->
  <section class="bg-{ac} text-white py-14 px-6 shadow-md">
    <div class="max-w-7xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
      <div>
        <div class="text-4xl md:text-6xl font-black mb-1">190+</div>
        <div class="text-xs uppercase font-extrabold tracking-widest opacity-90">Completed Buildings</div>
      </div>
      <div>
        <div class="text-4xl md:text-6xl font-black mb-1">32</div>
        <div class="text-xs uppercase font-extrabold tracking-widest opacity-90">Active Ongoing Sites</div>
      </div>
      <div>
        <div class="text-4xl md:text-6xl font-black mb-1">500+</div>
        <div class="text-xs uppercase font-extrabold tracking-widest opacity-90">Masons, Workers & Engineers</div>
      </div>
      <div>
        <div class="text-4xl md:text-6xl font-black mb-1">100%</div>
        <div class="text-xs uppercase font-extrabold tracking-widest opacity-90">On-Time Project Delivery</div>
      </div>
    </div>
  </section>

  <!-- 5. ABOUT US WITH EXTRA-LARGE IMAGES (h-[480px]) -->
  <section id="about" class="py-28 px-6 max-w-7xl mx-auto">
    <div class="grid lg:grid-cols-12 gap-14 items-center">
      <div class="lg:col-span-7 grid sm:grid-cols-2 gap-6">
        <div class="relative h-[480px] {rad} overflow-hidden shadow-2xl border border-gray-200">
          <img src="{t['about_imgs'][0]}" alt="Site Workers and Engineers" class="w-full h-full object-cover">
          <div class="absolute bottom-0 inset-x-0 bg-gradient-to-t from-black/80 to-transparent p-6 text-white">
            <span class="bg-{ac} text-white text-xs font-extrabold px-3 py-1 rounded">On-Site Workforce</span>
            <h4 class="text-xl font-black mt-2">Dedicated Civil Engineers & Masons</h4>
          </div>
        </div>
        <div class="relative h-[480px] {rad} overflow-hidden shadow-2xl border border-gray-200 sm:mt-10">
          <img src="{t['about_imgs'][1]}" alt="Building Structure" class="w-full h-full object-cover">
          <div class="absolute bottom-0 inset-x-0 bg-gradient-to-t from-black/80 to-transparent p-6 text-white">
            <span class="bg-emerald-600 text-white text-xs font-extrabold px-3 py-1 rounded">Heavy RCC Framing</span>
            <h4 class="text-xl font-black mt-2">Multi-Story Structural Execution</h4>
          </div>
        </div>
      </div>

      <div class="lg:col-span-5">
        <span class="bg-{bbg} text-{btxt} font-extrabold uppercase tracking-widest text-xs px-4 py-2 rounded-full">
          Registered Building Contractors
        </span>
        <h2 class="text-3xl sm:text-5xl font-black text-slate-900 mt-5 mb-6 leading-tight">
          Building High-Strength Concrete Landmarks
        </h2>
        <p class="text-slate-600 text-base leading-relaxed mb-6">
          <strong>{name}</strong> is a full-scale building construction company operating from <strong>{address}</strong>. We execute residential apartment towers, corporate office buildings, shopping complexes, institutional blocks, and industrial warehouses.
        </p>
        <p class="text-slate-600 text-sm leading-relaxed mb-8">
          Our in-house team of civil engineers, architectural planners, shuttering carpenters, steel bar-benders, and masons ensures every square foot meets IS-456 seismic safety standards using M30 Ready-Mix Concrete and Fe-550D TMT steel.
        </p>
        <div class="p-6 bg-gray-50 {rad} border border-gray-200 space-y-3 text-sm">
          <div><strong class="text-slate-900">Company Name:</strong> {name}</div>
          <div><strong class="text-slate-900">Direct Phone:</strong> <a href="tel:{phone}" class="text-{act} font-extrabold">{phone}</a></div>
          <div><strong class="text-slate-900">Corporate Email:</strong> <a href="mailto:{email}" class="text-{act} font-extrabold">{email}</a></div>
          <div><strong class="text-slate-900">Head Office:</strong> {address}</div>
        </div>
      </div>
    </div>
  </section>

  <!-- 6. GIANT ONGOING PROJECTS ("ADHURI BUILDINGS" - h-[420px] CARDS) -->
  <section id="ongoing" class="py-28 bg-gray-50 border-y border-gray-200 px-6">
    <div class="max-w-7xl mx-auto">
      <div class="text-center mb-16">
        <span class="bg-amber-100 text-amber-900 font-extrabold uppercase tracking-widest text-xs px-4 py-2 rounded-full">
          Live Under-Construction Projects
        </span>
        <h2 class="text-4xl md:text-6xl font-black text-slate-900 mt-4">Ongoing Building Construction Sites</h2>
        <p class="text-slate-600 text-base mt-3 max-w-3xl mx-auto">
          Large-scale buildings currently under active RCC column raising, slab shuttering, brickwork, and tower crane operations.
        </p>
      </div>

      <div class="grid lg:grid-cols-3 gap-10">
        {ongoing_cards}
      </div>
    </div>
  </section>

  <!-- 7. FULL-WIDTH PANORAMIC SITE SHOWCASE BANNER (h-[500px]) -->
  <section class="relative h-[500px] flex items-center justify-center overflow-hidden">
    <img src="{t['panorama_img']}" alt="Panoramic Construction Site" class="absolute inset-0 w-full h-full object-cover animate-live-bg">
    <div class="absolute inset-0 bg-slate-950/75"></div>
    <div class="relative z-10 max-w-5xl mx-auto px-6 text-center text-white">
      <span class="bg-{ac} text-white text-xs font-black uppercase tracking-widest px-4 py-2 rounded-full">
        Zero-Compromise Structural Engineering
      </span>
      <h2 class="text-4xl sm:text-6xl font-black mt-6 mb-6 leading-tight">
        From Deep Foundation Excavation To Final Key Handover
      </h2>
      <p class="text-lg text-gray-200 mb-8 max-w-3xl mx-auto">
        Every building constructed by <strong>{name}</strong> undergoes 40+ quality checkpoints including soil bearing tests, ultrasonic concrete scanning, and pressure waterproofing.
      </p>
      <a href="#contact" class="inline-block bg-white text-slate-950 hover:bg-gray-100 font-black px-10 py-4 {rad} shadow-2xl transition">
        Schedule Site Inspection — {phone}
      </a>
    </div>
  </section>

  <!-- 8. GIANT COMPLETED BUILDINGS ("BANI HUI BUILDINGS" - h-[450px] CARDS) -->
  <section id="completed" class="py-28 px-6 max-w-7xl mx-auto">
    <div class="text-center mb-16">
      <span class="bg-emerald-100 text-emerald-900 font-extrabold uppercase tracking-widest text-xs px-4 py-2 rounded-full">
        Delivered Landmarks
      </span>
      <h2 class="text-4xl md:text-6xl font-black text-slate-900 mt-4">Completed & Occupied Buildings</h2>
      <p class="text-slate-600 text-base mt-3 max-w-3xl mx-auto">
        Take a look at our finished commercial towers, residential apartment societies, and corporate complexes handed over on schedule.
      </p>
    </div>

    <div class="grid lg:grid-cols-3 gap-10">
      {completed_cards}
    </div>
  </section>

  <!-- 9. GIANT SITE WORKERS & ENGINEERS GALLERY (h-[390px] PORTRAITS) -->
  <section id="workforce" class="py-28 bg-gray-50 border-y border-gray-200 px-6">
    <div class="max-w-7xl mx-auto">
      <div class="text-center mb-16">
        <span class="bg-{bbg} text-{btxt} font-extrabold uppercase tracking-widest text-xs px-4 py-2 rounded-full">
          Our On-Ground Power
        </span>
        <h2 class="text-4xl md:text-6xl font-black text-slate-900 mt-4">Our Site Workers, Masons & Civil Engineers</h2>
        <p class="text-slate-600 text-base mt-3 max-w-3xl mx-auto">
          Trained bar-benders, shuttering carpenters, concrete masons, crane operators, and civil engineers working across all active sites of <strong>{name}</strong>.
        </p>
      </div>

      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-8">
        {worker_cards}
      </div>
    </div>
  </section>

  <!-- 10. HEAVY MACHINERY & QUALITY LABS (LARGE VISUAL CARDS) -->
  <section id="machinery" class="py-28 px-6 max-w-7xl mx-auto">
    <div class="text-center mb-16">
      <span class="bg-{bbg} text-{btxt} font-extrabold uppercase tracking-widest text-xs px-4 py-2 rounded-full">
        Plant & Equipment Fleet
      </span>
      <h2 class="text-4xl md:text-5xl font-black text-slate-900 mt-4">In-House Heavy Construction Machinery</h2>
    </div>

    <div class="grid md:grid-cols-3 gap-8">
      <div class="bg-white border border-gray-200 {rad} overflow-hidden shadow-lg hover-lift">
        <img src="https://images.unsplash.com/photo-1504917599217-d4dc5ebe6122?auto=format&fit=crop&w=900&q=85" class="w-full h-80 object-cover" alt="Tower Cranes">
        <div class="p-6">
          <h4 class="text-xl font-black text-slate-900 mb-2">Tower Cranes & Boom Placers</h4>
          <p class="text-sm text-slate-600">High-capacity tower cranes and mobile concrete boom pumps for rapid high-rise slab casting.</p>
        </div>
      </div>

      <div class="bg-white border border-gray-200 {rad} overflow-hidden shadow-lg hover-lift">
        <img src="https://images.unsplash.com/photo-1581094794329-c8112a89af12?auto=format&fit=crop&w=900&q=85" class="w-full h-80 object-cover" alt="RMC Batching">
        <div class="p-6">
          <h4 class="text-xl font-black text-slate-900 mb-2">Automated RMC Batching & Testing</h4>
          <p class="text-sm text-slate-600">Computerized concrete batching plants with on-site cube compression testing laboratories.</p>
        </div>
      </div>

      <div class="bg-white border border-gray-200 {rad} overflow-hidden shadow-lg hover-lift">
        <img src="https://images.unsplash.com/photo-1541888946425-d09bb18086f6?auto=format&fit=crop&w=900&q=85" class="w-full h-80 object-cover" alt="Excavators">
        <div class="p-6">
          <h4 class="text-xl font-black text-slate-900 mb-2">Heavy Excavators & Steel Yard</h4>
          <p class="text-sm text-slate-600">JCBs, Poclain rock-breakers, dumpers, and automated CNC TMT steel bar bending machines.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- 11. LEGAL ENTITY & STATUTORY VERIFICATION BLOCK -->
  <section class="py-20 bg-gray-50 border-t border-gray-200 px-6">
    <div class="max-w-5xl mx-auto bg-white border-2 border-slate-900 {rad} p-10 shadow-2xl">
      <div class="flex flex-wrap justify-between items-center gap-4 pb-6 mb-8 border-b border-gray-200">
        <div>
          <span class="text-xs font-extrabold uppercase tracking-widest text-{act}">Official Corporate Registry</span>
          <h3 class="text-3xl font-black text-slate-900">Verified Business Details</h3>
        </div>
        <span class="bg-emerald-100 text-emerald-800 text-xs font-black px-4 py-2 rounded-full">
          <i class="fa-solid fa-circle-check mr-1.5"></i> Active & Verified Entity
        </span>
      </div>

      <div class="grid md:grid-cols-2 gap-6 text-base">
        <div class="p-5 bg-gray-50 rounded-2xl border border-gray-200">
          <span class="text-xs font-bold uppercase text-slate-400 block mb-1">Business Legal Name</span>
          <span class="font-black text-slate-900 text-lg">{name}</span>
        </div>
        <div class="p-5 bg-gray-50 rounded-2xl border border-gray-200">
          <span class="text-xs font-bold uppercase text-slate-400 block mb-1">Official Phone Number</span>
          <a href="tel:{phone}" class="font-black text-{act} text-lg hover:underline">{phone}</a>
        </div>
        <div class="p-5 bg-gray-50 rounded-2xl border border-gray-200">
          <span class="text-xs font-bold uppercase text-slate-400 block mb-1">Official Email ID</span>
          <a href="mailto:{email}" class="font-black text-{act} text-lg hover:underline break-all">{email}</a>
        </div>
        <div class="p-5 bg-gray-50 rounded-2xl border border-gray-200">
          <span class="text-xs font-bold uppercase text-slate-400 block mb-1">Registered Office Address</span>
          <span class="font-black text-slate-900">{address}</span>
        </div>
      </div>
    </div>
  </section>

  <!-- 12. FOOTER WITH PROMINENT NAME, ADDRESS, PHONE & EMAIL -->
  <footer id="contact" class="bg-{dbg} text-white pt-20 pb-12 px-6 border-t-8 border-{ac}">
    <div class="max-w-7xl mx-auto grid lg:grid-cols-12 gap-12 pb-16 border-b border-slate-800">
      <div class="lg:col-span-5">
        <div class="flex items-center space-x-3 mb-6">
          <div class="w-11 h-11 rounded-xl bg-{ac} flex items-center justify-center text-white text-xl font-black">
            <i class="fa-solid fa-city"></i>
          </div>
          <span class="text-2xl font-black">{name}</span>
        </div>
        <p class="text-slate-400 text-sm leading-relaxed mb-8">
          Premier building construction and civil infrastructure company specializing in multi-story residential towers, commercial plazas, and turnkey RCC structures.
        </p>
        <div class="flex gap-4">
          <button onclick="openModal('loginModal')" class="bg-slate-800 hover:bg-{ac} text-white text-xs font-extrabold px-6 py-3 rounded-xl transition">Client Login</button>
          <button onclick="openModal('signupModal')" class="bg-{ac} hover:bg-{ach} text-white text-xs font-extrabold px-6 py-3 rounded-xl transition">Partner Sign Up</button>
        </div>
      </div>

      <div class="lg:col-span-7 grid sm:grid-cols-3 gap-6">
        <div class="bg-slate-900 p-6 rounded-2xl border border-slate-800">
          <i class="fa-solid fa-location-dot text-2xl text-{act} mb-3"></i>
          <h4 class="text-xs font-bold uppercase text-slate-400 mb-2">Registered Address</h4>
          <p class="text-sm font-bold text-white leading-relaxed">{address}</p>
        </div>
        <div class="bg-slate-900 p-6 rounded-2xl border border-slate-800">
          <i class="fa-solid fa-phone-volume text-2xl text-{act} mb-3"></i>
          <h4 class="text-xs font-bold uppercase text-slate-400 mb-2">Phone Number</h4>
          <a href="tel:{phone}" class="text-base font-black text-white hover:underline block">{phone}</a>
        </div>
        <div class="bg-slate-900 p-6 rounded-2xl border border-slate-800">
          <i class="fa-solid fa-envelope text-2xl text-{act} mb-3"></i>
          <h4 class="text-xs font-bold uppercase text-slate-400 mb-2">Official Email</h4>
          <a href="mailto:{email}" class="text-sm font-black text-white hover:underline break-all block">{email}</a>
        </div>
      </div>
    </div>

    <div class="max-w-7xl mx-auto pt-8 text-center sm:flex justify-between items-center text-xs text-slate-400">
      <p>© 2026 <strong>{name}</strong>. All Rights Reserved.</p>
      <p class="mt-2 sm:mt-0">Address: {address} | Phone: {phone} | Email: {email}</p>
    </div>
  </footer>

  <!-- LOGIN MODAL WITH CONTINUE WITH GOOGLE -->
  <div id="loginModal" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 hidden items-center justify-center p-4">
    <div class="bg-white text-slate-900 w-full max-w-md p-8 {rad} shadow-2xl relative">
      <button onclick="closeModal('loginModal')" class="absolute top-5 right-5 text-slate-400 hover:text-slate-900 text-xl"><i class="fa-solid fa-xmark"></i></button>
      <h3 class="text-2xl font-black mb-1">Client Portal Login</h3>
      <p class="text-xs text-slate-500 mb-6">Access project milestones & BOQ billing for {name}</p>

      <button onclick="alert('Redirecting to Google Sign-In...');" class="w-full bg-white hover:bg-gray-50 text-slate-800 font-bold py-3.5 px-4 rounded-xl border border-gray-300 flex items-center justify-center space-x-3 mb-5 shadow-sm">
        <svg class="w-5 h-5" viewBox="0 0 24 24">
          <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
          <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
          <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
          <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
        </svg>
        <span class="text-sm">Continue with Google</span>
      </button>

      <form onsubmit="event.preventDefault(); alert('Authenticated successfully!');" class="space-y-4 text-sm">
        <input type="email" required placeholder="Email Address" class="w-full bg-gray-50 border border-gray-300 rounded-xl px-4 py-3">
        <input type="password" required placeholder="Password" class="w-full bg-gray-50 border border-gray-300 rounded-xl px-4 py-3">
        <button type="submit" class="w-full bg-{ac} hover:bg-{ach} text-white font-extrabold py-3.5 rounded-xl shadow-lg">Log In</button>
      </form>
    </div>
  </div>

  <!-- SIGN UP MODAL WITH CONTINUE WITH GOOGLE -->
  <div id="signupModal" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 hidden items-center justify-center p-4">
    <div class="bg-white text-slate-900 w-full max-w-md p-8 {rad} shadow-2xl relative">
      <button onclick="closeModal('signupModal')" class="absolute top-5 right-5 text-slate-400 hover:text-slate-900 text-xl"><i class="fa-solid fa-xmark"></i></button>
      <h3 class="text-2xl font-black mb-1">Create Client Account</h3>
      <p class="text-xs text-slate-500 mb-6">Register with {name}</p>

      <button onclick="alert('Redirecting to Google Sign-Up...');" class="w-full bg-white hover:bg-gray-50 text-slate-800 font-bold py-3.5 px-4 rounded-xl border border-gray-300 flex items-center justify-center space-x-3 mb-5 shadow-sm">
        <svg class="w-5 h-5" viewBox="0 0 24 24">
          <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
          <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
          <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
          <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
        </svg>
        <span class="text-sm">Sign up with Google</span>
      </button>

      <form onsubmit="event.preventDefault(); alert('Account created successfully!');" class="space-y-3.5 text-sm">
        <input type="text" required placeholder="Full Name / Company Name" class="w-full bg-gray-50 border border-gray-300 rounded-xl px-4 py-3">
        <input type="tel" required placeholder="Mobile Number" class="w-full bg-gray-50 border border-gray-300 rounded-xl px-4 py-3">
        <input type="email" required placeholder="Email Address" class="w-full bg-gray-50 border border-gray-300 rounded-xl px-4 py-3">
        <input type="password" required placeholder="Create Password" class="w-full bg-gray-50 border border-gray-300 rounded-xl px-4 py-3">
        <button type="submit" class="w-full bg-slate-900 hover:bg-{ac} text-white font-extrabold py-3.5 rounded-xl shadow-lg transition">Create Account</button>
      </form>
    </div>
  </div>

  <script>
    function openModal(id) {{ document.getElementById(id).classList.add('modal-active'); }}
    function closeModal(id) {{ document.getElementById(id).classList.remove('modal-active'); }}

    const phrases = [
      "Multi-Story Commercial & Residential Towers",
      "Earthquake-Resistant RCC Framed Buildings",
      "Turnkey Industrial Sheds & Corporate Plazas",
      "Deep Foundation & Heavy Civil Infrastructure"
    ];
    let pIdx = 0, cIdx = 0, isDel = false;
    const tw = document.getElementById("typewriter");
    function runType() {{
      const cur = phrases[pIdx];
      tw.innerText = isDel ? cur.substring(0, cIdx--) : cur.substring(0, cIdx++);
      let spd = isDel ? 35 : 65;
      if (!isDel && cIdx > cur.length) {{ spd = 1800; isDel = true; }}
      else if (isDel && cIdx === 0) {{ isDel = false; pIdx = (pIdx + 1) % phrases.length; spd = 350; }}
      setTimeout(runType, spd);
    }}
    document.addEventListener("DOMContentLoaded", runType);
  </script>
</body>
</html>"""


def parse_details(text):
    data = {}
    for line in text.strip().split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            k, v = k.strip().lower(), v.strip()
            if "name" in k:
                data["name"] = v
            elif "phone" in k or "mobile" in k or "number" in k:
                data["phone"] = v
            elif "email" in k or "gmail" in k or "mail" in k:
                data["email"] = v
            elif "address" in k or "location" in k:
                data["address"] = v
    return data


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    msg = (
        "🏗️ *1-to-10 Sequential Building Construction Website Generator*\n\n"
        "Is bot me *10 Alag-Alag White-Theme Construction Interfaces* hain (Extra-Large Photos + Alag Live Videos + Alag Design).\n\n"
        "🔄 *Automatic 1-by-1 Sequence:*\n"
        "1st message ➔ *Website #1*\n"
        "2nd message ➔ *Website #2*\n"
        "3rd message ➔ *Website #3* ... (1 se 10 tak line se aayega)\n\n"
        "👇 *Bas ye 4 details bhejo:*\n"
        "`Name: Balaji Building Constructions`\n"
        "`Phone: +91 9876543210`\n"
        "`Email: info@heoo.in`\n"
        "`Address: Plot 14, Civil Lines, Jaipur, Rajasthan 302006`\n\n"
        "⚙️ *Optional:* `/reset` (Wapas #1 se start karne ke liye)"
    )
    bot.reply_to(message, msg, parse_mode="Markdown")


@bot.message_handler(commands=['reset'])
def reset_sequence(message):
    set_template_index(1)
    bot.reply_to(message, "✅ Sequence reset ho gaya! Ab agla website **Template #1 / 10** se start hoga.", parse_mode="Markdown")


@bot.message_handler(func=lambda message: True)
def generate_site(message):
    data = parse_details(message.text)
    if not all(k in data for k in ["name", "phone", "email", "address"]):
        bot.reply_to(
            message,
            "⚠️ *Saari 4 details sahi format me bhejo:*\n\n"
            "`Name: Business Name`\n"
            "`Phone: +91 9876543210`\n"
            "`Email: contact@heoo.in`\n"
            "`Address: Full Address`",
            parse_mode="Markdown"
        )
        return

    idx = get_next_template_index()
    template_cfg = TEMPLATES_DATA[idx]
    template_num = template_cfg["id"]
    next_num = (idx + 1) % 10 + 1

    html = generate_html_for_template(
        template_cfg,
        data["name"],
        data["phone"],
        data["email"],
        data["address"]
    )

    bio = io.BytesIO(html.encode("utf-8"))
    bio.name = "index.html"

    bot.send_document(
        message.chat.id,
        bio,
        caption=(
            f"✅ *Building Construction Website #{template_num} / 10 Ready!*\n"
            f"🎨 *Interface Style:* {template_cfg['theme_name']}\n\n"
            f"🏢 *Name:* {data['name']}\n"
            f"📞 *Phone:* {data['phone']}\n"
            f"📧 *Email:* {data['email']}\n"
            f"📍 *Address:* {data['address']}\n\n"
            f"⏭️ *Agली baar details bhejne par Website #{next_num} aayegi.*"
        ),
        parse_mode="Markdown"
    )


app = Flask(__name__)

@app.route('/')
def health():
    return "10-in-1 Sequential Construction Bot Live 24/7"

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
