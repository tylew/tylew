import React, { useMemo, useEffect, useRef, useState } from 'react'
import './index.css'

export default function App() {
  const [autoScroll, setAutoScroll] = useState(true)
  const crawlRef = useRef()
  const scrollOffset = useRef(0)

  // generate placeholder content
  const sections = useMemo(() => {
    const arr = []
    for (let i = 1; i <= 8; i++) {
      arr.push({
        title: `Section ${i}`,
        color: `hsl(${(i * 40) % 360},70%,50%)`,
        text: `This section explores part ${i} of the journey — 
               challenges rise and fade as the path stretches into infinity.`
      })
    }
    return arr
  }, [])

  // handle F key
  useEffect(() => {
    const handler = (e) => {
      if (e.key.toLowerCase() === 'f') setAutoScroll((v) => !v)
    }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [])

  // manual scroll pause detection
  useEffect(() => {
    let timeout
    const onScroll = () => {
      setAutoScroll(false)
      clearTimeout(timeout)
      timeout = setTimeout(() => setAutoScroll(true), 2000)
    }
    window.addEventListener('wheel', onScroll)
    return () => window.removeEventListener('wheel', onScroll)
  }, [])

  // manual animation loop
  useEffect(() => {
    let last = performance.now()
    const step = (t) => {
      const dt = t - last
      last = t
      if (autoScroll) {
        scrollOffset.current -= dt * 0.02 // speed
        if (crawlRef.current)
          crawlRef.current.style.transform = `rotateX(25deg) translateY(${scrollOffset.current}px) translateZ(-300px)`
      }
      requestAnimationFrame(step)
    }
    requestAnimationFrame(step)
  }, [autoScroll])

  return (
    <div className="crawl-root">
      <div className="stars">
        {Array.from({ length: 200 }).map((_, i) => (
          <div
            key={i}
            className="star"
            style={{
              top: Math.random() * 100 + '%',
              left: Math.random() * 100 + '%',
              animationDelay: `${Math.random() * 5}s`
            }}
          />
        ))}
      </div>

      <button
        className="toggle-btn"
        onClick={() => setAutoScroll((v) => !v)}
      >
        {autoScroll ? 'Pause' : 'Resume'}
      </button>

      <div className="crawl-container">
        <div ref={crawlRef} className="crawl">
          <h1>EPISODE 0</h1>
          <h2>The Infinite Scroll</h2>
          <p>
            In a boundless web, a single page drifts eternally through the
            void. Its words and colors stretch into the horizon, defying
            stillness and gravity alike.
          </p>

          {sections.map((s, i) => (
            <div key={i} className="section">
              <div
                className="placeholder"
                style={{ backgroundColor: s.color }}
              />
              <h3>{s.title}</h3>
              <p>{s.text}</p>
            </div>
          ))}

          <p>
            The crawl continues beyond sight, forever receding into the
            darkness. Press F or click Pause to stop the stars from moving.
          </p>
        </div>
      </div>
    </div>
  )
}