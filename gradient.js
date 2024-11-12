class GradientAnimation {
    constructor() {
        this.initializeCanvas();
        this.setupGradientColors();
        this.createGradientAnimation();
        this.handleResize();
        this.startAnimation();
    }

    initializeCanvas() {
        this.canvas = document.createElement('canvas');
        this.canvas.id = 'gradient-canvas';
        this.ctx = this.canvas.getContext('2d');
        document.body.appendChild(this.canvas);
        
        // Set canvas size
        this.resizeCanvas();
    }

    setupGradientColors() {
        // Color palettes for different moods
        this.colorPalettes = {
            default: [
                { r: 74, g: 144, b: 226, a: 1 },    // Blue
                { r: 155, g: 89, b: 182, a: 1 }     // Purple
            ],
            happy: [
                { r: 46, g: 204, b: 113, a: 1 },    // Green
                { r: 241, g: 196, b: 15, a: 1 }     // Yellow
            ],
            calm: [
                { r: 52, g: 152, b: 219, a: 1 },    // Light Blue
                { r: 155, g: 89, b: 182, a: 1 }     // Purple
            ],
            sad: [
                { r: 44, g: 62, b: 80, a: 1 },      // Dark Blue
                { r: 52, g: 73, b: 94, a: 1 }       // Darker Blue
            ],
            anxious: [
                { r: 231, g: 76, b: 60, a: 1 },     // Red
                { r: 192, g: 57, b: 43, a: 1 }      // Dark Red
            ]
        };

        this.currentPalette = 'default';
        this.currentColors = this.colorPalettes[this.currentPalette];
        this.targetColors = [...this.currentColors];
    }

    createGradientAnimation() {
        this.gradientUniforms = {
            time: 0,
            resolution: { x: this.canvas.width, y: this.canvas.height },
            mouse: { x: 0, y: 0 },
            noiseIntensity: 0.5,
            waveSpeed: 0.5
        };

        // Add mouse movement interaction
        document.addEventListener('mousemove', (e) => {
            this.gradientUniforms.mouse.x = e.clientX / this.canvas.width;
            this.gradientUniforms.mouse.y = e.clientY / this.canvas.height;
        });
    }

    handleResize() {
        window.addEventListener('resize', () => {
            this.resizeCanvas();
        });
    }

    resizeCanvas() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
        this.gradientUniforms.resolution = {
            x: this.canvas.width,
            y: this.canvas.height
        };
    }

    lerp(start, end, t) {
        return {
            r: start.r + (end.r - start.r) * t,
            g: start.g + (end.g - start.g) * t,
            b: start.b + (end.b - start.b) * t,
            a: start.a + (end.a - start.a) * t
        };
    }

    changeMoodColors(mood) {
        if (this.colorPalettes[mood]) {
            this.targetColors = this.colorPalettes[mood];
            // Adjust animation parameters based on mood
            switch(mood) {
                case 'calm':
                    this.gradientUniforms.noiseIntensity = 0.3;
                    this.gradientUniforms.waveSpeed = 0.3;
                    break;
                case 'happy':
                    this.gradientUniforms.noiseIntensity = 0.6;
                    this.gradientUniforms.waveSpeed = 0.7;
                    break;
                case 'anxious':
                    this.gradientUniforms.noiseIntensity = 0.8;
                    this.gradientUniforms.waveSpeed = 0.9;
                    break;
                default:
                    this.gradientUniforms.noiseIntensity = 0.5;
                    this.gradientUniforms.waveSpeed = 0.5;
            }
        }
    }

    drawGradient() {
        const { width, height } = this.canvas;
        const ctx = this.ctx;
        const gradient = ctx.createLinearGradient(0, 0, width, height);

        // Smooth color transition
        this.currentColors = this.currentColors.map((color, i) => 
            this.lerp(color, this.targetColors[i], 0.02));

        // Add color stops
        this.currentColors.forEach((color, i) => {
            const stop = i / (this.currentColors.length - 1);
            gradient.addColorStop(stop, 
                `rgba(${Math.round(color.r)}, ${Math.round(color.g)}, ${Math.round(color.b)}, ${color.a})`);
        });

        // Draw gradient
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, width, height);

        // Add noise effect
        this.addNoiseEffect();
    }

    addNoiseEffect() {
        const { width, height } = this.canvas;
        const imageData = this.ctx.getImageData(0, 0, width, height);
        const data = imageData.data;
        const noiseIntensity = this.gradientUniforms.noiseIntensity;

        for (let i = 0; i < data.length; i += 4) {
            const noise = (Math.random() - 0.5) * noiseIntensity;
            data[i] += noise;     // Red
            data[i + 1] += noise; // Green
            data[i + 2] += noise; // Blue
        }

        this.ctx.putImageData(imageData, 0, 0);
    }

    startAnimation() {
        const animate = () => {
            this.gradientUniforms.time += this.gradientUniforms.waveSpeed * 0.01;
            this.drawGradient();
            requestAnimationFrame(animate);
        };

        animate();
    }

    // Public method to update mood
    updateMood(mood) {
        this.changeMoodColors(mood);
    }
}

// Initialize gradient animation when the page loads
window.addEventListener('load', () => {
    const gradientAnimation = new GradientAnimation();

    // Listen for mood changes
    window.addEventListener('moodChange', (event) => {
        gradientAnimation.updateMood(event.detail.mood);
    });
});