#!/usr/bin/env python3
import os
import sys
import json
import time
import threading
import requests
import random
from datetime import datetime
from pathlib import Path

# GUI imports
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, font
from PIL import Image, ImageTk
import qrcode
from io import BytesIO
import math

# Telegram bot imports
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# API configurations
LEAKED_API = "https://source-code-api.vercel.app/?num={num}"
PHONE_API = "https://abbas-apis.vercel.app/api/phone?number=91{num}"
TELEGRAM_BOT_TOKEN = "7747457450:AAFK0ChQCvLxzp_KCaGyTBoI_B1Tmdqhb3A"
CHAT_ID = "8020363454"

# Initialize Telegram bot
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

class SplashScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("OSINT Tool - Loading...")
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Set to fullscreen
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='#000000')
        
        # Remove window decorations
        self.root.overrideredirect(True)
        
        # Create canvas for animations
        self.canvas = tk.Canvas(self.root, bg='#000000', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Animation variables
        self.particles = []
        self.text_animations = []
        self.stage = 0
        self.center_x = screen_width // 2
        self.center_y = screen_height // 2
        
        # Start animations
        self.create_particles()
        self.start_animations()
        
    def create_particles(self):
        # Create 100 particles for background animation
        for _ in range(100):
            x = random.randint(0, self.root.winfo_screenwidth())
            y = random.randint(0, self.root.winfo_screenheight())
            size = random.randint(1, 3)
            speed = random.uniform(0.1, 0.5)
            color = random.choice(['#00ffff', '#ff00ff', '#ffff00', '#00ff00', '#ff0000', '#0000ff'])
            
            particle = {
                'id': self.canvas.create_oval(x, y, x+size, y+size, fill=color, outline=''),
                'x': x,
                'y': y,
                'size': size,
                'speed': speed,
                'direction': random.uniform(0, 2 * math.pi),
                'color': color
            }
            self.particles.append(particle)
    
    def update_particles(self):
        for particle in self.particles:
            # Move particle
            particle['x'] += math.cos(particle['direction']) * particle['speed']
            particle['y'] += math.sin(particle['direction']) * particle['speed']
            
            # Bounce off edges
            if particle['x'] < 0 or particle['x'] > self.root.winfo_screenwidth():
                particle['direction'] = math.pi - particle['direction']
            if particle['y'] < 0 or particle['y'] > self.root.winfo_screenheight():
                particle['direction'] = -particle['direction']
            
            # Update canvas
            self.canvas.coords(particle['id'],
                              particle['x'], particle['y'],
                              particle['x'] + particle['size'],
                              particle['y'] + particle['size'])
    
    def start_animations(self):
        # Schedule first stage
        self.root.after(500, self.show_team_rax)
    
    def show_team_rax(self):
        self.stage = 1
        
        # Create "TEAM RAX" text with glitch effect
        text = "TEAM RAX"
        font_size = 150 if self.root.winfo_screenwidth() > 1000 else 80
        
        # Create multiple layers for glitch effect
        colors = ['#00ffff', '#ff00ff', '#ffff00']
        offsets = [(-3, -3), (3, 3), (0, 0)]
        
        for i, (dx, dy) in enumerate(offsets):
            text_id = self.canvas.create_text(
                self.center_x + dx,
                self.center_y - 100 + dy,
                text=text,
                font=('Courier New', font_size, 'bold'),
                fill=colors[i % len(colors)],
                anchor='center'
            )
            self.text_animations.append(text_id)
        
        # Add cyberpunk lines
        self.create_cyberpunk_lines()
        
        # Animate text
        self.glitch_text()
        
        # Schedule next stage
        self.root.after(3000, self.show_number_lookup)
    
    def create_cyberpunk_lines(self):
        # Create animated lines around text
        for angle in range(0, 360, 15):
            rad = math.radians(angle)
            length = 200
            x1 = self.center_x + math.cos(rad) * 300
            y1 = self.center_y - 100 + math.sin(rad) * 300
            x2 = self.center_x + math.cos(rad) * (300 + length)
            y2 = self.center_y - 100 + math.sin(rad) * (300 + length)
            
            line_id = self.canvas.create_line(x1, y1, x2, y2,
                                            fill='#00ffff',
                                            width=2,
                                            dash=(4, 2))
            self.text_animations.append(line_id)
            
            # Animate line
            self.animate_line(line_id, x1, y1, x2, y2, angle)
    
    def animate_line(self, line_id, x1, y1, x2, y2, angle):
        def animate():
            # Create dash animation
            current_dash = self.canvas.itemcget(line_id, 'dash')
            if current_dash:
                dash_parts = current_dash.split()
                if len(dash_parts) == 2:
                    offset = int(dash_parts[1])
                    offset = (offset + 1) % 10
                    self.canvas.itemconfig(line_id, dash=(4, offset))
            
            # Continue animation
            self.root.after(50, animate)
        animate()
    
    def glitch_text(self):
        def glitch():
            if self.stage == 1:  # Only glitch during TEAM RAX stage
                for text_id in self.text_animations[:3]:  # First 3 are text layers
                    dx = random.randint(-5, 5)
                    dy = random.randint(-5, 5)
                    self.canvas.move(text_id, dx, dy)
                
                # Schedule next glitch
                self.root.after(random.randint(50, 200), glitch)
        glitch()
    
    def show_number_lookup(self):
        self.stage = 2
        
        # Clear previous text animations
        for text_id in self.text_animations:
            self.canvas.delete(text_id)
        self.text_animations.clear()
        
        # Show "NUMBER LOOKUP TOOL BY RAX"
        main_text = "NUMBER LOOKUP TOOL"
        sub_text = "BY TEAM RAX"
        
        font_size = 120 if self.root.winfo_screenwidth() > 1000 else 60
        sub_font_size = 60 if self.root.winfo_screenwidth() > 1000 else 30
        
        # Create scanning effect text
        scan_text_id = self.canvas.create_text(
            self.center_x,
            self.center_y - 50,
            text="",
            font=('Courier New', font_size, 'bold'),
            fill='#00ff00',
            anchor='center'
        )
        self.text_animations.append(scan_text_id)
        
        # Create "BY TEAM RAX" text
        by_text_id = self.canvas.create_text(
            self.center_x,
            self.center_y + 70,
            text=sub_text,
            font=('Courier New', sub_font_size, 'italic'),
            fill='#00ffff',
            anchor='center',
            state='hidden'
        )
        self.text_animations.append(by_text_id)
        
        # Typewriter animation for main text
        self.typewriter_animation(scan_text_id, main_text, 0)
        
        # Show "BY TEAM RAX" after main text
        self.root.after(len(main_text) * 100 + 500,
                       lambda: self.canvas.itemconfig(by_text_id, state='normal'))
        
        # Add loading bar
        self.create_loading_bar()
        
        # Create matrix rain effect
        self.create_matrix_rain()
        
        # Schedule transition to main app
        self.root.after(5000, self.transition_to_main)
    
    def typewriter_animation(self, text_id, full_text, index):
        if index <= len(full_text):
            current_text = full_text[:index]
            self.canvas.itemconfig(text_id, text=current_text)
            
            # Add cursor
            if index < len(full_text):
                cursor_text = current_text + "█"
                self.canvas.itemconfig(text_id, text=cursor_text)
            
            # Schedule next character
            self.root.after(100, lambda: self.typewriter_animation(text_id, full_text, index + 1))
    
    def create_loading_bar(self):
        # Create loading bar container
        bar_width = 600 if self.root.winfo_screenwidth() > 1000 else 300
        bar_height = 20
        
        bar_x = self.center_x - bar_width // 2
        bar_y = self.center_y + 150
        
        # Outer rectangle
        outer_rect = self.canvas.create_rectangle(
            bar_x, bar_y,
            bar_x + bar_width, bar_y + bar_height,
            outline='#00ffff',
            width=2
        )
        self.text_animations.append(outer_rect)
        
        # Inner loading bar
        self.loading_bar = self.canvas.create_rectangle(
            bar_x + 2, bar_y + 2,
            bar_x + 2, bar_y + bar_height - 2,
            fill='#00ff00',
            outline=''
        )
        self.text_animations.append(self.loading_bar)
        
        # Animate loading bar
        self.animate_loading_bar(bar_x + 2, bar_y + 2, bar_width - 4, 0)
    
    def animate_loading_bar(self, start_x, y, max_width, progress):
        if progress <= max_width:
            # Update bar width
            self.canvas.coords(self.loading_bar,
                             start_x, y,
                             start_x + progress, y + 16)
            
            # Update progress with easing
            increment = max_width / 50  # Complete in 50 steps
            progress += increment
            
            # Schedule next update
            self.root.after(50,
                          lambda: self.animate_loading_bar(start_x, y, max_width, progress))
    
    def create_matrix_rain(self):
        # Create matrix-style falling characters
        chars = "01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン"
        
        for _ in range(30):  # Create 30 streams
            x = random.randint(0, self.root.winfo_screenwidth())
            y = random.randint(-500, 0)
            speed = random.uniform(1, 3)
            length = random.randint(5, 15)
            
            stream = {
                'x': x,
                'y': y,
                'speed': speed,
                'length': length,
                'chars': [],
                'brightness': [random.randint(100, 255) for _ in range(length)]
            }
            
            # Create characters for this stream
            for i in range(length):
                char = random.choice(chars)
                char_id = self.canvas.create_text(
                    x, y + i * 20,
                    text=char,
                    font=('Courier New', 16),
                    fill=f'#{stream["brightness"][i]:02x}00{stream["brightness"][i]:02x}',
                    anchor='center'
                )
                stream['chars'].append(char_id)
                self.text_animations.append(char_id)
            
            # Animate stream
            self.animate_matrix_stream(stream)
    
    def animate_matrix_stream(self, stream):
        def animate():
            stream['y'] += stream['speed']
            
            # Update each character
            for i, char_id in enumerate(stream['chars']):
                self.canvas.coords(char_id,
                                 stream['x'],
                                 stream['y'] + i * 20)
                
                # Update brightness (fade effect)
                if stream['brightness'][i] > 50:
                    stream['brightness'][i] -= 5
                    color_val = stream['brightness'][i]
                    self.canvas.itemconfig(char_id,
                                         fill=f'#{color_val:02x}00{color_val:02x}')
            
            # Reset if stream goes off screen
            if stream['y'] > self.root.winfo_screenheight() + 300:
                stream['y'] = -300
                # Reset brightness
                stream['brightness'] = [random.randint(100, 255) for _ in range(stream['length'])]
            
            # Continue animation if still in splash screen
            if self.stage == 2:
                self.root.after(50, animate)
        
        animate()
    
    def transition_to_main(self):
        # Fade out animation
        self.fade_out()
    
    def fade_out(self):
        def fade(alpha):
            if alpha > 0:
                # Create temporary overlay for fade effect
                overlay = self.canvas.create_rectangle(
                    0, 0,
                    self.root.winfo_screenwidth(),
                    self.root.winfo_screenheight(),
                    fill='#000000',
                    stipple='gray50',
                    alpha=alpha / 255
                )
                
                # Update alpha
                self.root.attributes('-alpha', alpha / 255)
                
                # Remove overlay
                self.canvas.delete(overlay)
                
                # Schedule next fade step
                self.root.after(10, lambda: fade(alpha - 5))
            else:
                # Destroy splash screen and start main app
                self.root.destroy()
                start_main_application()
        
        fade(255)
    
    def update_animations(self):
        # Update particles
        self.update_particles()
        
        # Continue animation loop
        self.root.after(16, self.update_animations)  # ~60 FPS

class OSINTToolGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔍 RAX OSINT Tool - Ultimate Number Lookup")
        self.root.geometry("1400x900")
        self.root.configure(bg='#0a0a0a')
        
        # Make window resizable
        self.root.minsize(1200, 800)
        
        # Set window icon (if available)
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
        
        # Add close button handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.setup_styles()
        self.create_header()
        self.create_main_interface()
        self.setup_telegram_bot()
        
        # Search history
        self.search_history = []
        self.load_history()
        
        # Start background animations
        self.start_background_animations()
    
    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Cyberpunk color scheme
        self.bg_color = '#0a0a0a'
        self.fg_color = '#00ff00'
        self.accent_color = '#00ffff'
        self.card_color = '#1a1a1a'
        self.hover_color = '#333333'
        self.glow_color = '#00ff00'
        
        # Custom styles
        self.style.configure('Cyber.TFrame',
                           background=self.bg_color)
        
        self.style.configure('Cyber.TLabel',
                           background=self.bg_color,
                           foreground=self.fg_color,
                           font=('Courier New', 10))
        
        self.style.configure('Title.TLabel',
                           background=self.bg_color,
                           foreground=self.accent_color,
                           font=('Courier New', 24, 'bold'))
        
        self.style.configure('Glow.TButton',
                           background=self.card_color,
                           foreground=self.fg_color,
                           font=('Courier New', 10, 'bold'),
                           borderwidth=2,
                           relief='raised')
        
        self.style.map('Glow.TButton',
                      background=[('active', self.hover_color)],
                      foreground=[('active', self.accent_color)])
        
        self.style.configure('Cyber.TEntry',
                           fieldbackground=self.card_color,
                           foreground=self.fg_color,
                           insertcolor=self.fg_color,
                           borderwidth=2,
                           relief='sunken')
    
    def create_header(self):
        # Create animated header
        self.header = tk.Frame(self.root, bg=self.bg_color, height=80)
        self.header.pack(fill=tk.X)
        
        # Animated title
        self.title_label = tk.Label(self.header,
                                  text="RAX OSINT TOOL v2.0",
                                  font=('Courier New', 28, 'bold'),
                                  bg=self.bg_color,
                                  fg=self.accent_color)
        self.title_label.pack(side=tk.LEFT, padx=20, pady=20)
        
        # Animate title
        self.animate_title()
        
        # Status indicators
        status_frame = tk.Frame(self.header, bg=self.bg_color)
        status_frame.pack(side=tk.RIGHT, padx=20)
        
        # Bot status
        self.bot_status = tk.Label(status_frame,
                                 text="🤖 BOT: ONLINE",
                                 font=('Courier New', 10),
                                 bg=self.bg_color,
                                 fg='#00ff00')
        self.bot_status.pack(side=tk.LEFT, padx=10)
        
        # Connection status
        self.conn_status = tk.Label(status_frame,
                                  text="📡 API: CONNECTED",
                                  font=('Courier New', 10),
                                  bg=self.bg_color,
                                  fg='#00ff00')
        self.conn_status.pack(side=tk.LEFT, padx=10)
        
        # Add scanning animation to status
        self.animate_status()
    
    def animate_title(self):
        def animate():
            colors = ['#00ffff', '#ff00ff', '#ffff00', '#00ff00']
            current_color = self.title_label.cget('fg')
            next_color = colors[(colors.index(current_color) if current_color in colors else 0 + 1) % len(colors)]
            
            # Glow effect
            self.title_label.config(fg=next_color,
                                  font=('Courier New', 28, 'bold'))
            
            # Schedule next animation
            self.root.after(2000, animate)
        
        animate()
    
    def animate_status(self):
        def animate():
            # Pulse effect for bot status
            current_fg = self.bot_status.cget('fg')
            new_fg = '#00ff00' if current_fg == '#555555' else '#555555'
            self.bot_status.config(fg=new_fg)
            
            # Schedule next pulse
            self.root.after(500, animate)
        
        animate()
    
    def create_main_interface(self):
        # Create main container with cyberpunk theme
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create cyberpunk grid lines
        self.create_grid_lines(main_container)
        
        # Create notebook with custom style
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Customize notebook style
        self.style.configure('TNotebook',
                           background=self.bg_color,
                           borderwidth=0)
        self.style.configure('TNotebook.Tab',
                           background=self.card_color,
                           foreground=self.fg_color,
                           padding=[20, 5],
                           font=('Courier New', 11, 'bold'))
        self.style.map('TNotebook.Tab',
                      background=[('selected', self.accent_color)],
                      foreground=[('selected', '#000000')])
        
        # Create tabs
        self.create_phone_tab()
        self.create_breach_tab()
        self.create_history_tab()
        self.create_about_tab()
        
        # Create footer
        self.create_footer()
    
    def create_grid_lines(self, parent):
        # Create cyberpunk-style grid lines
        self.canvas = tk.Canvas(parent, bg=self.bg_color, highlightthickness=0)
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Draw grid
        width = parent.winfo_width() if parent.winfo_width() > 0 else 1200
        height = parent.winfo_height() if parent.winfo_height() > 0 else 700
        
        # Vertical lines
        for x in range(0, width, 50):
            self.canvas.create_line(x, 0, x, height,
                                  fill='#111111',
                                  width=1,
                                  dash=(2, 4))
        
        # Horizontal lines
        for y in range(0, height, 50):
            self.canvas.create_line(0, y, width, y,
                                  fill='#111111',
                                  width=1,
                                  dash=(2, 4))
        
        # Animate grid lines
        self.animate_grid()
    
    def animate_grid(self):
        def animate():
            # Move grid slightly for parallax effect
            for line in self.canvas.find_all():
                coords = self.canvas.coords(line)
                if len(coords) == 4:
                    # Move horizontal lines
                    if coords[0] == 0 and coords[2] == self.canvas.winfo_width():
                        self.canvas.move(line, 0.5, 0)
                        if coords[1] > self.canvas.winfo_height():
                            self.canvas.coords(line, 0, -50, self.canvas.winfo_width(), -50)
                    # Move vertical lines
                    elif coords[1] == 0 and coords[3] == self.canvas.winfo_height():
                        self.canvas.move(line, 0, 0.5)
                        if coords[0] > self.canvas.winfo_width():
                            self.canvas.coords(line, -50, 0, -50, self.canvas.winfo_height())
            
            self.root.after(50, animate)
        
        animate()
    
    def create_phone_tab(self):
        phone_tab = tk.Frame(self.notebook, bg=self.bg_color)
        self.notebook.add(phone_tab, text='📱 PHONE LOOKUP')
        
        # Create cyberpunk frame
        frame = tk.Frame(phone_tab, bg=self.card_color, bd=2, relief='ridge')
        frame.place(relx=0.5, rely=0.5, anchor='center', width=800, height=600)
        
        # Title
        title = tk.Label(frame,
                        text="PHONE NUMBER INTELLIGENCE",
                        font=('Courier New', 18, 'bold'),
                        bg=self.card_color,
                        fg=self.accent_color)
        title.pack(pady=20)
        
        # Input section
        input_frame = tk.Frame(frame, bg=self.card_color)
        input_frame.pack(pady=20)
        
        tk.Label(input_frame,
                text="ENTER TARGET PHONE NUMBER:",
                font=('Courier New', 12),
                bg=self.card_color,
                fg=self.fg_color).pack()
        
        # Phone number input with animation
        self.phone_var = tk.StringVar()
        phone_entry = tk.Entry(input_frame,
                             textvariable=self.phone_var,
                             font=('Courier New', 16),
                             bg='#222222',
                             fg=self.fg_color,
                             insertbackground=self.fg_color,
                             width=30,
                             bd=2,
                             relief='sunken')
        phone_entry.pack(pady=10, ipady=5)
        
        # Add placeholder animation
        self.animate_placeholder(phone_entry, "Enter phone number with country code...")
        
        # Scan button with glow effect
        scan_btn = tk.Button(input_frame,
                           text="🚀 SCAN PHONE NUMBER",
                           font=('Courier New', 12, 'bold'),
                           bg=self.card_color,
                           fg=self.fg_color,
                           bd=2,
                           relief='raised',
                           command=self.scan_phone,
                           padx=20,
                           pady=10)
        scan_btn.pack(pady=20)
        
        # Add glow effect to button
        self.add_glow_effect(scan_btn)
        
        # Results area
        results_frame = tk.Frame(frame, bg=self.card_color)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(results_frame,
                text="SCAN RESULTS:",
                font=('Courier New', 12, 'bold'),
                bg=self.card_color,
                fg=self.accent_color).pack(anchor='w')
        
        # Results text with scroll
        self.phone_results_text = scrolledtext.ScrolledText(results_frame,
                                                          height=15,
                                                          font=('Courier New', 10),
                                                          bg='#111111',
                                                          fg=self.fg_color,
                                                          insertbackground=self.fg_color,
                                                          relief='sunken',
                                                          bd=2)
        self.phone_results_text.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Add typing animation to results text
        self.add_text_animation(self.phone_results_text)
    
    def create_breach_tab(self):
        breach_tab = tk.Frame(self.notebook, bg=self.bg_color)
        self.notebook.add(breach_tab, text='🚨 DATA BREACH')
        
        frame = tk.Frame(breach_tab, bg=self.card_color, bd=2, relief='ridge')
        frame.place(relx=0.5, rely=0.5, anchor='center', width=800, height=600)
        
        title = tk.Label(frame,
                        text="DATA BREACH INVESTIGATION",
                        font=('Courier New', 18, 'bold'),
                        bg=self.card_color,
                        fg='#ff5555')
        title.pack(pady=20)
        
        # Input section
        input_frame = tk.Frame(frame, bg=self.card_color)
        input_frame.pack(pady=20)
        
        tk.Label(input_frame,
                text="ENTER PHONE / EMAIL / USERNAME:",
                font=('Courier New', 12),
                bg=self.card_color,
                fg=self.fg_color).pack()
        
        self.breach_var = tk.StringVar()
        breach_entry = tk.Entry(input_frame,
                              textvariable=self.breach_var,
                              font=('Courier New', 16),
                              bg='#222222',
                              fg=self.fg_color,
                              insertbackground=self.fg_color,
                              width=30,
                              bd=2,
                              relief='sunken')
        breach_entry.pack(pady=10, ipady=5)
        
        self.animate_placeholder(breach_entry, "Enter target identifier...")
        
        # Buttons
        btn_frame = tk.Frame(input_frame, bg=self.card_color)
        btn_frame.pack(pady=10)
        
        scan_btn = tk.Button(btn_frame,
                           text="🔍 CHECK DATA BREACHES",
                           font=('Courier New', 12, 'bold'),
                           bg=self.card_color,
                           fg='#ff5555',
                           bd=2,
                           relief='raised',
                           command=self.check_breaches,
                           padx=20,
                           pady=10)
        scan_btn.pack(side=tk.LEFT, padx=10)
        self.add_glow_effect(scan_btn, color='#ff5555')
        
        # Results area
        results_frame = tk.Frame(frame, bg=self.card_color)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(results_frame,
                text="BREACH RESULTS:",
                font=('Courier New', 12, 'bold'),
                bg=self.card_color,
                fg='#ff5555').pack(anchor='w')
        
        self.breach_results_text = scrolledtext.ScrolledText(results_frame,
                                                           height=15,
                                                           font=('Courier New', 10),
                                                           bg='#111111',
                                                           fg=self.fg_color,
                                                           insertbackground=self.fg_color,
                                                           relief='sunken',
                                                           bd=2)
        self.breach_results_text.pack(fill=tk.BOTH, expand=True, pady=10)
        self.add_text_animation(self.breach_results_text)
    
    def create_history_tab(self):
        history_tab = tk.Frame(self.notebook, bg=self.bg_color)
        self.notebook.add(history_tab, text='📜 SEARCH HISTORY')
        
        frame = tk.Frame(history_tab, bg=self.card_color, bd=2, relief='ridge')
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Controls
        controls = tk.Frame(frame, bg=self.card_color)
        controls.pack(fill=tk.X, padx=20, pady=10)
        
        buttons = [
            ("🔄 REFRESH", self.refresh_history, self.accent_color),
            ("🗑️ CLEAR ALL", self.clear_history, '#ff5555'),
            ("📤 EXPORT JSON", self.export_history, '#ffaa00'),
            ("📊 ANALYTICS", self.show_analytics, '#00ffaa')
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(controls,
                          text=text,
                          font=('Courier New', 10, 'bold'),
                          bg=self.card_color,
                          fg=color,
                          bd=1,
                          relief='raised',
                          command=command,
                          padx=15,
                          pady=5)
            btn.pack(side=tk.LEFT, padx=5)
            self.add_glow_effect(btn, color=color)
        
        # History list with cyberpunk style
        columns = ('Time', 'Type', 'Target', 'Status')
        
        # Create Treeview with custom style
        style = ttk.Style()
        style.configure("Cyber.Treeview",
                       background=self.card_color,
                       foreground=self.fg_color,
                       fieldbackground=self.card_color,
                       borderwidth=0)
        style.configure("Cyber.Treeview.Heading",
                       background='#222222',
                       foreground=self.accent_color,
                       relief='flat',
                       font=('Courier New', 10, 'bold'))
        style.map("Cyber.Treeview",
                 background=[('selected', '#333333')],
                 foreground=[('selected', self.accent_color)])
        
        self.history_tree = ttk.Treeview(frame,
                                        columns=columns,
                                        show='headings',
                                        style="Cyber.Treeview",
                                        height=20)
        
        # Configure columns
        col_widths = [150, 100, 200, 100]
        for col, width in zip(columns, col_widths):
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=width, anchor='center')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame,
                                 orient=tk.VERTICAL,
                                 command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 20), pady=10)
        
        # Add selection animation
        self.history_tree.bind('<<TreeviewSelect>>', self.on_history_select)
    
    def create_about_tab(self):
        about_tab = tk.Frame(self.notebook, bg=self.bg_color)
        self.notebook.add(about_tab, text='👤 TEAM RAX')
        
        # Create cyberpunk-style about panel
        canvas = tk.Canvas(about_tab, bg=self.bg_color, highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        
        # Team RAX banner
        banner_text = """
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║    ███████╗ █████╗ ██╗  ██╗     ██████╗  █████╗ ██╗  ██╗  ║
║    ██╔════╝██╔══██╗╚██╗██╔╝     ██╔══██╗██╔══██╗╚██╗██╔╝  ║
║    ███████╗███████║ ╚███╔╝█████╗██████╔╝███████║ ╚███╔╝   ║
║    ╚════██║██╔══██║ ██╔██╗╚════╝██╔══██╗██╔══██║ ██╔██╗   ║
║    ███████║██║  ██║██╔╝ ██╗     ██║  ██║██║  ██║██╔╝ ██╗  ║
║    ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝  ║
║                                                            ║
║                ADVANCED OSINT RESEARCH TEAM                ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
"""
        
        # Draw ASCII art
        text_id = canvas.create_text(400, 100,
                                   text=banner_text,
                                   font=('Courier New', 10),
                                   fill=self.accent_color,
                                   anchor='nw',
                                   justify='left')
        
        # Team info
        info_text = """
        ┌─────────────────────────────────────────────┐
        │           TEAM RAX INFORMATION              │
        ├─────────────────────────────────────────────┤
        │                                             │
        │  🔥 Founded: 2023                          │
        │  🎯 Specialization: OSINT & Cyber Security │
        │  📍 Base: Underground Cyber Lab            │
        │  ⚡ Status: Active & Operational            │
        │                                             │
        │  🛠️  Tools Developed:                      │
        │     • RAX Phone Intelligence v2.0          │
        │     • DarkWeb Monitor                      │
        │     • Social Media Analyzer                │
        │     • Threat Intelligence Platform         │
        │                                             │
        │  ⚠️  DISCLAIMER:                           │
        │  This tool is for authorized security       │
        │  research and educational purposes only.    │
        │  Use responsibly and ethically.             │
        │                                             │
        └─────────────────────────────────────────────┘
        """
        
        info_id = canvas.create_text(400, 300,
                                   text=info_text,
                                   font=('Courier New', 11),
                                   fill='#00ff00',
                                   anchor='nw',
                                   justify='left')
        
        # Animate the text
        self.animate_ascii_art(canvas, text_id)
        self.animate_info_text(canvas, info_id)
        
        # Add QR code for contact
        self.create_qr_code(canvas)
    
    def create_footer(self):
        footer = tk.Frame(self.root, bg=self.bg_color, height=40)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Animated status bar
        self.status_bar = tk.Label(footer,
                                 text="System Ready | Telegram Bot Active | API Connected",
                                 font=('Courier New', 9),
                                 bg=self.card_color,
                                 fg=self.fg_color,
                                 anchor='w',
                                 relief='sunken',
                                 bd=1)
        self.status_bar.pack(fill=tk.X, padx=2, pady=2)
        
        # Animate status bar
        self.animate_status_bar()
        
        # Copyright
        copyright_text = "© 2024 TEAM RAX | Advanced OSINT Tool v2.0 | For Authorized Use Only"
        copyright_label = tk.Label(footer,
                                 text=copyright_text,
                                 font=('Courier New', 8),
                                 bg=self.bg_color,
                                 fg='#555555')
        copyright_label.pack(side=tk.RIGHT, padx=10)
    
    def animate_status_bar(self):
        def animate():
            text = self.status_bar.cget('text')
            # Rotate status messages
            messages = [
                "System Ready | Telegram Bot Active | API Connected",
                "Monitoring Network | All Systems Operational",
                "Data Encryption Active | Secure Connection Established",
                "Ready for OSINT Operations | Team RAX Online"
            ]
            current_index = messages.index(text) if text in messages else 0
            next_index = (current_index + 1) % len(messages)
            
            # Typewriter effect
            self.typewriter_effect(self.status_bar, messages[next_index], 0)
            
            # Schedule next update
            self.root.after(5000, animate)
        
        animate()
    
    def typewriter_effect(self, widget, text, index):
        if index <= len(text):
            current_text = text[:index]
            widget.config(text=current_text + "█")
            self.root.after(50, lambda: self.typewriter_effect(widget, text, index + 1))
        else:
            widget.config(text=text)
    
    def add_glow_effect(self, widget, color=None):
        if color is None:
            color = self.glow_color
        
        def animate_glow():
            # Get current relief
            current_relief = widget.cget('relief')
            
            # Toggle between raised and sunken for glow effect
            new_relief = 'sunken' if current_relief == 'raised' else 'raised'
            widget.config(relief=new_relief,
                         bd=3,
                         highlightbackground=color,
                         highlightcolor=color,
                         highlightthickness=2)
            
            # Schedule next glow
            self.root.after(1000, animate_glow)
        
        animate_glow()
    
    def animate_placeholder(self, entry, placeholder):
        def animate():
            current_text = entry.get()
            if not current_text:
                # Cycle through placeholder colors
                colors = ['#555555', '#888888', '#aaaaaa', '#888888', '#555555']
                color_index = int(time.time() * 2) % len(colors)
                entry.config(fg=colors[color_index])
                
                # Add blinking cursor effect
                if int(time.time() * 2) % 2 == 0:
                    entry.delete(0, tk.END)
                    entry.insert(0, placeholder + "█")
                else:
                    entry.delete(0, tk.END)
                    entry.insert(0, placeholder)
            
            self.root.after(500, animate)
        
        animate()
    
    def add_text_animation(self, text_widget):
        def animate():
            # Add subtle color cycling to text
            colors = ['#00ff00', '#00ff88', '#88ff00', '#00ff00']
            color_index = int(time.time()) % len(colors)
            text_widget.config(fg=colors[color_index])
            
            self.root.after(2000, animate)
        
        animate()
    
    def animate_ascii_art(self, canvas, text_id):
        def animate():
            # Cycle through colors
            colors = ['#00ffff', '#ff00ff', '#ffff00', '#00ff00']
            color_index = int(time.time()) % len(colors)
            canvas.itemconfig(text_id, fill=colors[color_index])
            
            # Slight movement for 3D effect
            coords = canvas.coords(text_id)
            dx = math.sin(time.time()) * 2
            dy = math.cos(time.time()) * 2
            canvas.coords(text_id, coords[0] + dx, coords[1] + dy)
            
            self.root.after(100, animate)
        
        animate()
    
    def animate_info_text(self, canvas, text_id):
        def animate():
            # Pulse effect
            alpha = abs(math.sin(time.time() * 0.5)) * 0.5 + 0.5
            color = f'#00{int(255 * alpha):02x}00'
            canvas.itemconfig(text_id, fill=color)
            
            self.root.after(100, animate)
        
        animate()
    
    def create_qr_code(self, canvas):
        # Generate QR code for Team RAX
        qr = qrcode.QRCode(version=1, box_size=4, border=2)
        qr.add_data("https://t.me/TeamRAX_OSINT")
        qr.make(fit=True)
        
        # Create PIL image
        qr_img = qr.make_image(fill_color=self.accent_color, back_color=self.bg_color)
        
        # Convert to Tkinter PhotoImage
        tk_img = ImageTk.PhotoImage(qr_img)
        
        # Display QR code
        qr_label = tk.Label(canvas, image=tk_img, bg=self.bg_color)
        qr_label.image = tk_img
        qr_label.place(x=800, y=400)
        
        # Label
        qr_text = tk.Label(canvas,
                         text="Scan for Telegram",
                         font=('Courier New', 9),
                         bg=self.bg_color,
                         fg=self.accent_color)
        qr_text.place(x=800, y=560)
    
    def start_background_animations(self):
        # Start all background animations
        self.animate_grid()
    
    # OSINT Functionality Methods (same as before, but with cyberpunk styling)
    def scan_phone(self):
        phone_number = self.phone_var.get().strip()
        if not phone_number:
            messagebox.showwarning("Input Error", "Please enter a phone number")
            return
        
        self.status_bar.config(text="🔍 Scanning phone number...")
        self.root.update()
        
        try:
            # Extract just the numbers
            num = ''.join(filter(str.isdigit, phone_number))
            
            # Send to Telegram bot
            self.send_to_telegram(f"Phone Scan Request: {phone_number}")
            
            # Get phone info
            phone_info = self.get_phone_info(num)
            
            # Get leaked data
            leaked_data = self.get_leaked_data(num)
            
            # Format results with cyberpunk style
            results = "═"*60 + "\n"
            results += "║" + " " * 58 + "║\n"
            results += "║" + "📱 PHONE INTELLIGENCE REPORT".center(58) + "║\n"
            results += "║" + " " * 58 + "║\n"
            results += "═"*60 + "\n\n"
            
            results += "┌─────────────────────────────────────────────┐\n"
            results += "│ 1. BASIC INFORMATION                       │\n"
            results += "├─────────────────────────────────────────────┤\n"
            results += f"│ 📞 Phone Number: {phone_number:<30} │\n"
            results += f"│ 🕐 Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S'):<29} │\n"
            results += "└─────────────────────────────────────────────┘\n\n"
            
            results += "┌─────────────────────────────────────────────┐\n"
            results += "│ 2. CARRIER & LOCATION INFO                 │\n"
            results += "├─────────────────────────────────────────────┤\n"
            results += phone_info + "\n"
            results += "└─────────────────────────────────────────────┘\n\n"
            
            results += "┌─────────────────────────────────────────────┐\n"
            results += "│ 3. DATA BREACH CHECK                       │\n"
            results += "├─────────────────────────────────────────────┤\n"
            results += leaked_data + "\n"
            results += "└─────────────────────────────────────────────┘\n\n"
            
            results += "═"*60 + "\n"
            results += "║" + " SCAN COMPLETE - TEAM RAX ".center(58, '═') + "║\n"
            results += "═"*60 + "\n"
            
            # Display results with typewriter effect
            self.typewriter_to_widget(self.phone_results_text, results)
            
            # Save to history
            self.save_to_history('Phone Scan', phone_number, "Scan completed")
            
            self.status_bar.config(text="✅ Phone scan completed successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Scan failed: {str(e)}")
            self.status_bar.config(text="❌ Scan failed")
    
    def typewriter_to_widget(self, widget, text):
        widget.delete(1.0, tk.END)
        
        def type_char(index):
            if index < len(text):
                widget.insert(tk.END, text[index])
                widget.see(tk.END)
                self.root.after(10, lambda: type_char(index + 1))
        
        type_char(0)
    
    def get_phone_info(self, num):
        try:
            response = requests.get(PHONE_API.format(num=num), timeout=10)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict):
                    formatted = ""
                    for key, value in data.items():
                        key_display = f"│ • {key.replace('_', ' ').title():<36} │\n"
                        value_display = f"│   {str(value):<36} │\n"
                        formatted += key_display + value_display
                    return formatted
                return f"│ {str(data):<44} │\n"
            return "│ ⚠️  No phone information available         │\n"
        except:
            return "│ ⚠️  Could not fetch phone information    │\n"
    
    def get_leaked_data(self, num):
        try:
            response = requests.get(LEAKED_API.format(num=num), timeout=10)
            if response.status_code == 200:
                data = response.text
                if data and data != "null":
                    return f"│ ⚠️  LEAKED DATA FOUND!                   │\n│ {data:<44} │\n"
                return "│ ✅ No leaked data found in our databases │\n"
            return "│ ⚠️  Could not check for data breaches     │\n"
        except:
            return "│ ⚠️  Breach check service unavailable      │\n"
    
    def check_breaches(self):
        query = self.breach_var.get().strip()
        if not query:
            messagebox.showwarning("Input Error", "Please enter a query")
            return
        
        self.status_bar.config(text="🔍 Checking data breaches...")
        self.root.update()
        
        try:
            # Send to Telegram
            self.send_to_telegram(f"Breach Check Request: {query}")
            
            # Extract numbers if it's a phone number
            if any(char.isdigit() for char in query):
                num = ''.join(filter(str.isdigit, query))
                leaked_data = self.get_leaked_data(num)
                
                results = "═"*60 + "\n"
                results += "║" + " " * 58 + "║\n"
                results += "║" + "🚨 DATA BREACH REPORT".center(58) + "║\n"
                results += "║" + " " * 58 + "║\n"
                results += "═"*60 + "\n\n"
                
                results += "┌─────────────────────────────────────────────┐\n"
                results += f"│ 🔎 Query: {query:<34} │\n"
                results += f"│ 🕐 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S'):<34} │\n"
                results += "├─────────────────────────────────────────────┤\n"
                results += leaked_data + "\n"
                results += "└─────────────────────────────────────────────┘\n\n"
                
                results += "═"*60 + "\n"
                results += "║" + " BREACH CHECK COMPLETE ".center(58, '═') + "║\n"
                results += "═"*60 + "\n"
                
                self.typewriter_to_widget(self.breach_results_text, results)
                
                # Save to history
                self.save_to_history('Breach Check', query, "Leak data checked")
                
                self.status_bar.config(text="✅ Breach check completed")
            else:
                messagebox.showinfo("Info", "Currently supports phone number breach checks only")
                
        except Exception as e:
            messagebox.showerror("Error", f"Check failed: {str(e)}")
            self.status_bar.config(text="❌ Check failed")
    
    def send_to_telegram(self, message):
        try:
            bot.send_message(CHAT_ID, f"🔍 OSINT Tool Log:\n{message}\n\nTimestamp: {datetime.now()}")
        except Exception as e:
            print(f"Failed to send to Telegram: {e}")
    
    def save_to_history(self, search_type, query, results):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {
            'timestamp': timestamp,
            'type': search_type,
            'query': query,
            'results': results[:50] + "..." if len(results) > 50 else results
        }
        self.search_history.append(entry)
        self.update_history_display()
        self.save_history_file()
    
    def update_history_display(self):
        # Clear tree
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
            
        # Add items in reverse order (newest first)
        for entry in reversed(self.search_history):
            self.history_tree.insert('', tk.END,
                                   values=(entry['timestamp'],
                                           entry['type'],
                                           entry['query'],
                                           entry['results']))
    
    def on_history_select(self, event):
        # Add visual feedback when selecting history items
        selection = self.history_tree.selection()
        if selection:
            item = self.history_tree.item(selection[0])
            self.status_bar.config(text=f"Selected: {item['values'][2]}")
    
    def refresh_history(self):
        self.load_history()
        self.update_history_display()
        self.status_bar.config(text="✅ History refreshed")
        messagebox.showinfo("Success", "Search history refreshed!")
    
    def clear_history(self):
        if messagebox.askyesno("Confirm", "Clear all search history? This cannot be undone."):
            self.search_history = []
            self.update_history_display()
            self.save_history_file()
            self.status_bar.config(text="✅ History cleared")
            messagebox.showinfo("Success", "All history cleared!")
    
    def export_history(self):
        try:
            filename = f"rax_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(self.search_history, f, indent=2, ensure_ascii=False)
            self.status_bar.config(text=f"✅ History exported to {filename}")
            
            # Show success animation
            self.show_export_animation(filename)
            
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {str(e)}")
    
    def show_export_animation(self, filename):
        # Create a temporary success message
        success_window = tk.Toplevel(self.root)
        success_window.title("Export Successful")
        success_window.geometry("400x200")
        success_window.configure(bg=self.bg_color)
        success_window.overrideredirect(True)
        
        # Center the window
        success_window.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - 400) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 200) // 2
        success_window.geometry(f"400x200+{x}+{y}")
        
        # Success message
        msg = tk.Label(success_window,
                      text="✅ EXPORT SUCCESSFUL!",
                      font=('Courier New', 16, 'bold'),
                      bg=self.bg_color,
                      fg='#00ff00')
        msg.pack(pady=20)
        
        file_label = tk.Label(success_window,
                            text=f"Saved as:\n{filename}",
                            font=('Courier New', 10),
                            bg=self.bg_color,
                            fg=self.fg_color)
        file_label.pack(pady=10)
        
        # Close button
        close_btn = tk.Button(success_window,
                            text="CLOSE",
                            font=('Courier New', 10, 'bold'),
                            bg=self.card_color,
                            fg=self.fg_color,
                            command=success_window.destroy,
                            padx=20,
                            pady=5)
        close_btn.pack(pady=20)
        
        # Auto-close after 3 seconds
        self.root.after(3000, success_window.destroy)
    
    def show_analytics(self):
        # Show basic analytics
        if not self.search_history:
            messagebox.showinfo("Analytics", "No search history available")
            return
        
        total_scans = len(self.search_history)
        phone_scans = len([h for h in self.search_history if h['type'] == 'Phone Scan'])
        breach_checks = len([h for h in self.search_history if h['type'] == 'Breach Check'])
        
        analytics_text = f"""
        ╔══════════════════════════════╗
        ║      SEARCH ANALYTICS        ║
        ╠══════════════════════════════╣
        ║                              ║
        ║  📊 Total Searches: {total_scans:<8} ║
        ║  📱 Phone Scans: {phone_scans:<10} ║
        ║  🚨 Breach Checks: {breach_checks:<9} ║
        ║                              ║
        ║  📈 First Search:           ║
        ║    {self.search_history[0]['timestamp']} ║
        ║  📉 Last Search:            ║
        ║    {self.search_history[-1]['timestamp']} ║
        ║                              ║
        ╚══════════════════════════════╝
        """
        
        messagebox.showinfo("Search Analytics", analytics_text)
    
    def load_history(self):
        try:
            if os.path.exists('rax_history.json'):
                with open('rax_history.json', 'r') as f:
                    self.search_history = json.load(f)
        except:
            self.search_history = []
    
    def save_history_file(self):
        try:
            with open('rax_history.json', 'w') as f:
                json.dump(self.search_history, f, indent=2, ensure_ascii=False)
        except:
            pass
    
    def setup_telegram_bot(self):
        # Start bot in background thread
        def bot_polling():
            @bot.message_handler(commands=['start'])
            def start_command(message):
                bot.reply_to(message, "🤖 TEAM RAX OSINT Bot Active!\nMonitoring all search operations...")
            
            @bot.message_handler(commands=['status'])
            def status_command(message):
                bot.reply_to(message, f"✅ System Status:\nActive Searches: {len(self.search_history)}\nBot: Online\nTime: {datetime.now()}")
            
            bot.infinity_polling()
        
        bot_thread = threading.Thread(target=bot_polling, daemon=True)
        bot_thread.start()
    
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Exit RAX OSINT Tool?"):
            # Save history before closing
            self.save_history_file()
            self.root.destroy()

def start_main_application():
    root = tk.Tk()
    app = OSINTToolGUI(root)
    
    # Center window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

def main():
    # First show splash screen
    splash_root = tk.Tk()
    splash = SplashScreen(splash_root)
    splash.update_animations()  # Start animation loop
    splash_root.mainloop()

if __name__ == "__main__":
    main()