import re
import os

files = [
    "screen_cdece41ffcb74a918d41d6bde21779ba.html", # Hero
    "screen_93fce9eccd3d40cab4787685ecd86d75.html", # Categories
    "screen_24237488251b4a45b06da75ac321d214.html", # Methodology
    "screen_9f304bf6e2ea4cdc863c8ec3afd5cbff.html", # Publications
    "screen_b64885b5a98543e6a57c92c1acd5d90e.html"  # Contact
]

sections = []
head_content = ""

for idx, f in enumerate(files):
    if not os.path.exists(f): continue
    with open(f, "r", encoding='utf8') as fp:
        html = fp.read()
    
    if idx == 0:
        head_match = re.search(r'<head>(.*?)</head>', html, re.DOTALL)
        if head_match:
            head_content = head_match.group(1)
            
    body_match = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL)
    if body_match:
        body_content = body_match.group(1)
        
        body_content = body_content.replace('fixed inset-0', 'absolute inset-0')
        body_content = body_content.replace('fixed top-0', 'absolute top-0')
        body_content = body_content.replace('fixed bottom-8', 'absolute bottom-8')
        body_content = body_content.replace('fixed right-8', 'absolute right-8')
        
        sections.append(f'<section id="slide-{idx}" class="w-full min-h-screen relative flex flex-col shrink-0 overflow-hidden bg-background-dark">\n{body_content}\n</section>')


intro_html = """
    <div id="dynamic-island-container">
        <nav class="dynamic-island" id="dynamic-island">
            <div class="island-visible">
                <span class="material-symbols-outlined" style="font-size: 20px;">science</span>
                <span>Laboratory</span>
            </div>
            <div class="island-hidden nav-links">
                <a href="#slide-0">Введение</a>
                <a href="#slide-1">Направления</a>
                <a href="#slide-2">Методология</a>
                <a href="#slide-3">Публикации</a>
                <a href="#slide-4">Запись</a>
            </div>
        </nav>
    </div>

    <div id="intro-sequence" class="relative z-0" style="height: 400vh;">
        <div class="sticky top-0 left-0 w-full h-screen overflow-hidden bg-[#070707] flex items-center justify-center">
            
            <div id="video-wrapper" class="absolute top-0 left-0 w-full h-full">
                <!-- CANVAS VIDEO -->
                <canvas id="bg-canvas" class="absolute top-0 left-0 w-full h-full object-cover"></canvas>
                
                <!-- OVERLAY FOR FADEOUT TO BLACK -->
                <div id="fade-overlay" class="absolute inset-0 bg-background-dark opacity-0 pointer-events-none z-20"></div>
                
                <!-- SVG BACTERIA CONTAINER -->
                <div id="bacteria-container" class="absolute inset-0 pointer-events-none z-10"></div>
            </div>
            
            <!-- TEXT HINT -->
            <div id="scroll-hint" class="absolute bottom-10 left-1/2 -translate-x-1/2 text-gray-400 font-mono text-xs uppercase tracking-widest text-center transition-opacity flex flex-col items-center gap-2 z-30">
                Скролльте вниз
                <div class="w-[1px] h-8 bg-gray-400 animate-pulse"></div>
            </div>
        </div>
    </div>
"""

script_content = """
    <style>
        /* --- DYNAMIC ISLAND (НАВИГАЦИЯ СВЕРХУ) APPLE LIQUID GLASS --- */
        .dynamic-island {
            position: fixed;
            top: 24px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(15, 15, 15, 0.5);
            backdrop-filter: blur(30px);
            -webkit-backdrop-filter: blur(30px);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 30px;
            padding: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
            overflow: hidden;
            /* Пружинящая (желейная) анимация Apple */
            transition: all 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
            width: 170px;
            height: 52px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        }

        .island-visible {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 15px;
            font-weight: 500;
            opacity: 1;
            /* Смещение вверх при открытии */
            transition: all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            white-space: nowrap;
        }

        .island-hidden {
            display: flex;
            gap: 24px;
            opacity: 0;
            visibility: hidden;
            position: absolute;
            transition: opacity 0.4s ease 0.1s, transform 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
            transform: scale(0.8) translateY(15px);
            white-space: nowrap;
        }

        .island-hidden a {
            color: rgba(255,255,255,0.7);
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
            transition: color 0.3s ease;
        }

        .island-hidden a:hover {
            color: #fff;
        }

        .dynamic-island:hover {
            width: 580px;
            height: 64px;
            background: rgba(25, 25, 25, 0.8);
            border-radius: 32px;
            box-shadow: 0 15px 50px rgba(0, 0, 0, 0.7), inset 0 1px 0 rgba(255, 255, 255, 0.15);
        }

        .dynamic-island:hover .island-visible {
            opacity: 0;
            visibility: hidden;
            transform: translate(-50%, -150%) scale(0.8);
        }

        .dynamic-island:hover .island-hidden {
            opacity: 1;
            visibility: visible;
            transform: scale(1) translateY(0);
        }
        
        /* Hide existing headers in stitch slides to prevent dual navbars */
        section header {
            display: none !important;
        }
    </style>
    <script>
        const canvas = document.getElementById('bg-canvas');
        const ctx = canvas.getContext('2d');
        const frameCount = 120;
        const frames = [];
        let canvasWidth, canvasHeight;

        // Path to the provided sequence frames
        const getFramePath = (index) => `sequence1/ezgif-frame-${index.toString().padStart(3, '0')}.jpg`;

        function resizeCanvas() {
            canvasWidth = window.innerWidth;
            canvasHeight = window.innerHeight;
            canvas.width = canvasWidth;
            canvas.height = canvasHeight;
            renderFrame(currentFrameIndex);
        }

        window.addEventListener('resize', resizeCanvas);
        
        function renderFrame(index) {
            if (frames[index] && frames[index].complete && frames[index].naturalWidth !== 0) {
                const img = frames[index];
                const imgRatio = img.naturalWidth / img.naturalHeight;
                const canvasRatio = canvasWidth / canvasHeight;
                let drawWidth, drawHeight, offsetX, offsetY;

                if (imgRatio > canvasRatio) {
                    drawHeight = canvasHeight;
                    drawWidth = img.naturalWidth * (canvasHeight / img.naturalHeight);
                    offsetX = (canvasWidth - drawWidth) / 2;
                    offsetY = 0;
                } else {
                    drawWidth = canvasWidth;
                    drawHeight = img.naturalHeight * (canvasWidth / img.naturalWidth);
                    offsetX = 0;
                    offsetY = (canvasHeight - drawHeight) / 2;
                }

                ctx.fillStyle = "white";
                ctx.fillRect(0, 0, canvasWidth, canvasHeight);
                ctx.drawImage(img, offsetX, offsetY, drawWidth, drawHeight);
            }
        }

        // LOAD FRAMES
        for (let i = 1; i <= frameCount; i++) {
            const img = new Image();
            img.src = getFramePath(i);
            frames.push(img);
        }

        let currentFrameIndex = 0;
        // initial render loop to cover load time
        function drawLoop() {
            renderFrame(currentFrameIndex);
            requestAnimationFrame(drawLoop);
        }
        drawLoop();
        resizeCanvas();

        // ---- SVG BACTERIA LOGIC ---- //
        const bacteriaContainer = document.getElementById('bacteria-container');
        const bacteriaArray = [];
        const numBacteria = 60;
        
        const colors = [
            { stroke: 'rgba(19, 182, 236, 0.4)', fill: 'rgba(19, 182, 236, 0.1)', core: 'rgba(19, 182, 236, 0.5)' },
            { stroke: 'rgba(40, 200, 150, 0.4)', fill: 'rgba(40, 200, 150, 0.1)', core: 'rgba(40, 200, 150, 0.5)' },
            { stroke: 'rgba(150, 150, 200, 0.4)', fill: 'rgba(150, 150, 200, 0.1)', core: 'rgba(150, 150, 200, 0.5)' },
            { stroke: 'rgba(255, 100, 150, 0.4)', fill: 'rgba(255, 100, 150, 0.1)', core: 'rgba(255, 100, 150, 0.5)' }
        ];

        for (let i = 0; i < numBacteria; i++) {
            const c = colors[Math.floor(Math.random() * colors.length)];
            const svgNS = "http://www.w3.org/2000/svg";
            const svg = document.createElementNS(svgNS, "svg");
            svg.setAttribute("viewBox", "0 0 100 100");
            svg.style.position = 'absolute';
            
            const left = Math.random() * 95;
            const top = Math.random() * 95;
            svg.style.left = left + "%";
            svg.style.top = top + "%";
            
            const size = Math.random() * 60 + 20;
            svg.style.width = size + "px";
            svg.style.height = size + "px";
            
            svg.style.opacity = '0';
            svg.style.transform = `scale(0) rotate(0deg)`;
            svg.style.transition = 'transform 0.1s ease-out, opacity 0.1s ease-out';
            
            const cell = document.createElementNS(svgNS, "circle");
            cell.setAttribute("cx", "50");
            cell.setAttribute("cy", "50");
            cell.setAttribute("r", "40");
            cell.setAttribute("fill", c.fill);
            cell.setAttribute("stroke", c.stroke);
            cell.setAttribute("stroke-width", "3");
            
            const numCores = Math.floor(Math.random() * 3) + 1;
            for(let j = 0; j < numCores; j++) {
                const core = document.createElementNS(svgNS, "circle");
                core.setAttribute("cx", 50 + (Math.random() * 30 - 15));
                core.setAttribute("cy", 50 + (Math.random() * 30 - 15));
                core.setAttribute("r", Math.random() * 8 + 3);
                core.setAttribute("fill", c.core);
                svg.appendChild(core);
            }
            
            svg.appendChild(cell);
            
            for(let j=0; j<8; j++) {
                 const line = document.createElementNS(svgNS, "line");
                 const angle = (j / 8) * Math.PI * 2;
                 line.setAttribute("x1", 50 + Math.cos(angle)*40);
                 line.setAttribute("y1", 50 + Math.sin(angle)*40);
                 line.setAttribute("x2", 50 + Math.cos(angle)*(45 + Math.random()*10));
                 line.setAttribute("y2", 50 + Math.sin(angle)*(45 + Math.random()*10));
                 line.setAttribute("stroke", c.stroke);
                 line.setAttribute("stroke-width", "2");
                 line.setAttribute("stroke-linecap", "round");
                 svg.appendChild(line);
            }

            bacteriaContainer.appendChild(svg);
            
            bacteriaArray.push({
                el: svg,
                activationPoint: Math.random() * 0.8,
                speed: Math.random() * 2 + 0.5,
                directionX: (Math.random() - 0.5),
                directionY: (Math.random() - 0.5),
                rotSpeed: (Math.random() - 0.5) * 100
            });
        }

        // ---- SCROLL LOGIC ---- //
        const introSequence = document.getElementById('intro-sequence');
        const hint = document.getElementById('scroll-hint');
        const fadeOverlay = document.getElementById('fade-overlay');

        window.addEventListener('scroll', () => {
            const scrollTop = window.scrollY;
            const introHeight = introSequence.offsetHeight;
            const scrollableIntro = introHeight - window.innerHeight;
            
            let introProgress = scrollTop / scrollableIntro;
            if (introProgress < 0) introProgress = 0;
            if (introProgress > 1) introProgress = 1;

            if (introProgress > 0.02) {
                hint.style.opacity = '0';
            } else {
                hint.style.opacity = '1';
            }

            // Phases:
            // 0.0 -> 0.4 : Video Phase
            // 0.4 -> 0.7 : Bacteria Phase
            // 0.7 -> 1.0 : Fade out Phase

            const videoPhaseEnd = 0.4;
            const bacteriaPhaseEnd = 0.7;
            
            if (introProgress <= videoPhaseEnd) {
                // Video phase
                let videoProgress = introProgress / videoPhaseEnd;
                currentFrameIndex = Math.floor(videoProgress * (frameCount - 1));
                fadeOverlay.style.opacity = '0';
                
                bacteriaArray.forEach(b => {
                    b.el.style.opacity = '0';
                    b.el.style.transform = 'scale(0) rotate(0deg)';
                });
                
            } else if (introProgress <= bacteriaPhaseEnd) {
                // Bacteria phase
                currentFrameIndex = frameCount - 1; // Last white frame
                fadeOverlay.style.opacity = '0';
                
                let bacteriaProgress = (introProgress - videoPhaseEnd) / (bacteriaPhaseEnd - videoPhaseEnd);
                
                bacteriaArray.forEach(b => {
                    if (bacteriaProgress > b.activationPoint) {
                        let innerProgress = (bacteriaProgress - b.activationPoint) / (1 - b.activationPoint);
                        let scale = Math.min(innerProgress * 3, 1 + (innerProgress * 0.5));
                        let rotation = innerProgress * b.rotSpeed;
                        
                        b.el.style.opacity = Math.min(innerProgress * 5, 1);
                        b.el.style.transform = `scale(${scale}) rotate(${rotation}deg) translate(${b.directionX * innerProgress * 50}px, ${b.directionY * innerProgress * 50}px)`;
                    } else {
                        b.el.style.opacity = '0';
                        b.el.style.transform = 'scale(0) rotate(0deg)';
                    }
                });
            } else {
                // Fade out to black phase smoothly
                currentFrameIndex = frameCount - 1;
                let fadeProgress = (introProgress - bacteriaPhaseEnd) / (1 - bacteriaPhaseEnd);
                
                // Overlay opacity from 0 to 1 matches bg-background-dark seamlessly
                fadeOverlay.style.opacity = fadeProgress;
                
                bacteriaArray.forEach(b => {
                    b.el.style.opacity = Math.max(1 - (fadeProgress * 1.5), 0);
                });
            }
        });
        
        window.dispatchEvent(new Event('scroll'));
        
        // Navigation Dynamic Island Click Handlers
        document.querySelectorAll('.nav-links a').forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const targetId = this.getAttribute('href').substring(1);
                const targetSection = document.getElementById(targetId);
                
                if (targetSection) {
                    window.scrollTo({
                        top: targetSection.offsetTop,
                        behavior: 'smooth'
                    });
                }
            });
        });
    </script>
"""

final_html = f"""<!DOCTYPE html>
<html class="dark" lang="ru" style="scroll-behavior: smooth;">
<head>
{head_content}
</head>
<body class="bg-background-dark font-display text-slate-100 overflow-x-hidden selection:bg-primary/30 m-0">
    
    {intro_html}

    <div id="main-site" class="relative z-20 bg-background-dark">
        {''.join(sections)}
    </div>
    
    {script_content}

</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as out:
    out.write(final_html)
