import React, { useEffect, useRef } from 'react';

interface OceanCanvasBackgroundProps {
  intensity?: number;
  className?: string;
}

export const OceanCanvasBackground: React.FC<OceanCanvasBackgroundProps> = ({
  intensity = 1,
  className = ''
}) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationFrameId: number;
    let width = (canvas.width = canvas.parentElement?.clientWidth || window.innerWidth);
    let height = (canvas.height = canvas.parentElement?.clientHeight || window.innerHeight);

    // Particle current stream system
    const particleCount = Math.min(80, Math.floor(width / 20));
    const particles: Array<{
      x: number;
      y: number;
      speed: number;
      size: number;
      alpha: number;
      angle: number;
      color: string;
    }> = [];

    const colors = [
      'rgba(14, 165, 233, ', // Sky 500
      'rgba(56, 189, 248, ', // Sky 400
      'rgba(6, 182, 212, ',  // Cyan 500
      'rgba(125, 211, 252, ', // Sky 300
      'rgba(255, 255, 255, '  // White froth/glimmer
    ];

    for (let i = 0; i < particleCount; i++) {
      particles.push({
        x: Math.random() * width,
        y: Math.random() * height,
        speed: (0.3 + Math.random() * 0.7) * intensity,
        size: 1 + Math.random() * 2.5,
        alpha: 0.2 + Math.random() * 0.5,
        angle: (Math.random() - 0.5) * 0.4 + 0.1,
        color: colors[Math.floor(Math.random() * colors.length)]
      });
    }

    let time = 0;

    const handleResize = () => {
      if (!canvas || !canvas.parentElement) return;
      width = canvas.width = canvas.parentElement.clientWidth;
      height = canvas.height = canvas.parentElement.clientHeight;
    };

    const resizeObserver = new ResizeObserver(handleResize);
    if (canvas.parentElement) {
      resizeObserver.observe(canvas.parentElement);
    }

    // Dynamic wave simulation
    const drawWave = (
      yOffset: number,
      amplitude: number,
      frequency: number,
      speed: number,
      fillGradient: CanvasGradient | string,
      strokeColor?: string
    ) => {
      ctx.beginPath();
      ctx.moveTo(0, height);
      ctx.lineTo(0, yOffset);

      for (let x = 0; x <= width; x += 8) {
        // Multi-frequency wave formula
        const wave1 = Math.sin(x * frequency + time * speed) * amplitude;
        const wave2 = Math.cos(x * (frequency * 0.6) - time * (speed * 0.7)) * (amplitude * 0.4);
        const wave3 = Math.sin(x * (frequency * 1.5) + time * (speed * 1.2)) * (amplitude * 0.2);
        const y = yOffset + wave1 + wave2 + wave3;
        ctx.lineTo(x, y);
      }

      ctx.lineTo(width, height);
      ctx.closePath();

      ctx.fillStyle = fillGradient;
      ctx.fill();

      if (strokeColor) {
        ctx.strokeStyle = strokeColor;
        ctx.lineWidth = 1.5;
        ctx.stroke();
      }
    };

    const render = () => {
      time += 0.015 * intensity;
      ctx.clearRect(0, 0, width, height);

      // 1. Base light ocean bathymetric gradient
      const baseGrad = ctx.createLinearGradient(0, 0, width, height);
      baseGrad.addColorStop(0, '#E0F2FE');   // Light ocean blue-white
      baseGrad.addColorStop(0.3, '#BAE6FD'); // Azure tint
      baseGrad.addColorStop(0.7, '#7DD3FC'); // Crisp sky ocean
      baseGrad.addColorStop(1, '#38BDF8');   // Oceanic deep light blue
      ctx.fillStyle = baseGrad;
      ctx.fillRect(0, 0, width, height);

      // 2. Caustic light wave swirls in background
      const causticGrad = ctx.createRadialGradient(
        width * 0.4 + Math.sin(time * 0.8) * 80,
        height * 0.35 + Math.cos(time * 0.7) * 50,
        20,
        width * 0.4,
        height * 0.35,
        width * 0.6
      );
      causticGrad.addColorStop(0, 'rgba(255, 255, 255, 0.45)');
      causticGrad.addColorStop(0.5, 'rgba(186, 230, 253, 0.25)');
      causticGrad.addColorStop(1, 'rgba(125, 211, 252, 0)');
      ctx.fillStyle = causticGrad;
      ctx.fillRect(0, 0, width, height);

      // 3. Deep harmonic swell wave (Layer 1 - deep blue translucent)
      const grad1 = ctx.createLinearGradient(0, height * 0.45, 0, height);
      grad1.addColorStop(0, 'rgba(14, 165, 233, 0.18)');
      grad1.addColorStop(1, 'rgba(2, 132, 199, 0.35)');
      drawWave(height * 0.52, 35, 0.002, 1.2, grad1, 'rgba(255, 255, 255, 0.3)');

      // 4. Mid harmonic swell wave (Layer 2 - turquoise cyan shimmer)
      const grad2 = ctx.createLinearGradient(0, height * 0.58, 0, height);
      grad2.addColorStop(0, 'rgba(6, 182, 212, 0.22)');
      grad2.addColorStop(1, 'rgba(3, 105, 161, 0.4)');
      drawWave(height * 0.64, 28, 0.0035, -0.9, grad2, 'rgba(255, 255, 255, 0.4)');

      // 5. Foreground crest wave (Layer 3 - crystalline azure with foam rim)
      const grad3 = ctx.createLinearGradient(0, height * 0.72, 0, height);
      grad3.addColorStop(0, 'rgba(125, 211, 252, 0.28)');
      grad3.addColorStop(1, 'rgba(14, 116, 144, 0.45)');
      drawWave(height * 0.76, 22, 0.005, 1.6, grad3, 'rgba(255, 255, 255, 0.65)');

      // 6. Floating Current Particles / Bio-luminescent Marine Drift
      for (let i = 0; i < particles.length; i++) {
        const p = particles[i];
        p.x += Math.cos(p.angle) * p.speed + Math.sin(time + p.y * 0.01) * 0.4;
        p.y += Math.sin(p.angle) * (p.speed * 0.4) + Math.cos(time + p.x * 0.01) * 0.3;

        // Wrap around boundaries smoothly
        if (p.x < -10) p.x = width + 10;
        if (p.x > width + 10) p.x = -10;
        if (p.y < -10) p.y = height + 10;
        if (p.y > height + 10) p.y = -10;

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fillStyle = `${p.color}${p.alpha})`;
        ctx.shadowColor = 'rgba(255, 255, 255, 0.8)';
        ctx.shadowBlur = 6;
        ctx.fill();
        ctx.shadowBlur = 0;
      }

      animationFrameId = requestAnimationFrame(render);
    };

    render();

    return () => {
      cancelAnimationFrame(animationFrameId);
      resizeObserver.disconnect();
    };
  }, [intensity]);

  return (
    <canvas
      ref={canvasRef}
      className={`pointer-events-none absolute inset-0 h-full w-full ${className}`}
    />
  );
};
