#!/usr/bin/env python3
"""Generates about.html, events.html, projects.html, team.html, contact.html
from shared HEADER/FOOTER blocks + per-page <main> content.
index.html was already hand-written and is left untouched."""

import os

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | Rowan IEEE</title>
<meta name="description" content="{desc}">
<link rel="icon" href="favicon.ico">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Bricolage+Grotesque:wght@500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">
</head>
<body class="circuit-bg">
"""

HEADER = """
<header class="site-header">
  <div class="nav-wrap">
    <a href="index.html" class="brand">
      <img class="torch" src="images/ieee-torch.png" alt="IEEE" width="34" height="34">
      <span>Rowan IEEE<small>STUDENT BRANCH &middot; REGION 2</small></span>
    </a>
    <nav class="nav-links">
      <a href="index.html">Home</a>
      <a href="about.html">About</a>
      <a href="events.html">Events</a>
      <a href="projects.html">Showcase</a>
      <a href="team.html">Team</a>
      <a href="contact.html">Contact</a>
    </nav>
    <div class="nav-cta">
      <a class="btn btn-primary" href="https://discord.com/invite/ZesVYMSJWe" target="_blank" rel="noopener">Join our Discord</a>
      <button class="nav-toggle" aria-label="Toggle menu" aria-expanded="false">
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M2 5h16M2 10h16M2 15h16" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>
      </button>
    </div>
  </div>
</header>
"""

FOOTER = """
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <div class="brand" style="margin-bottom:12px;">
          <img class="torch" src="images/ieee-torch.png" alt="IEEE" width="30" height="30">
          <span>Rowan IEEE</span>
        </div>
        <p style="max-width:280px;">Rowan University's IEEE Student Branch, part of IEEE Region 2. Open to students of all majors.</p>
        <div class="social-row" style="justify-content:flex-start;">
          <a href="https://discord.com/invite/ZesVYMSJWe" target="_blank" rel="noopener" aria-label="Discord"><svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor"><path d="M20.3 4.9A19.8 19.8 0 0 0 15.6 3.3c-.2.4-.5 1-.7 1.4a18.3 18.3 0 0 0-5.8 0c-.2-.5-.4-1-.7-1.4A19.7 19.7 0 0 0 3.7 4.9C1 8.9.3 12.8.6 16.7a19.9 19.9 0 0 0 6 3c.5-.6.9-1.3 1.3-2a13 13 0 0 1-2-1c.2-.1.3-.3.5-.4a14.2 14.2 0 0 0 12.2 0l.4.4c-.6.4-1.3.7-2 1 .4.7.8 1.4 1.3 2a19.8 19.8 0 0 0 6-3c.4-4.5-.7-8.4-3-11.8ZM8.8 14.3c-1 0-1.8-.9-1.8-2s.8-2 1.8-2 1.8.9 1.8 2-.8 2-1.8 2Zm6.4 0c-1 0-1.8-.9-1.8-2s.8-2 1.8-2 1.8.9 1.8 2-.8 2-1.8 2Z"/></svg></a>
          <a href="https://www.instagram.com/rowanieee/" target="_blank" rel="noopener" aria-label="Instagram"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2c2.7 0 3.1 0 4.1.1 1.1 0 1.8.2 2.5.5.7.3 1.2.6 1.7 1.1.5.5.9 1 1.1 1.7.3.7.4 1.4.5 2.5 0 1 .1 1.4.1 4.1s0 3.1-.1 4.1c0 1.1-.2 1.8-.5 2.5-.3.7-.6 1.2-1.1 1.7-.5.5-1 .9-1.7 1.1-.7.3-1.4.4-2.5.5-1 0-1.4.1-4.1.1s-3.1 0-4.1-.1c-1.1 0-1.8-.2-2.5-.5-.7-.3-1.2-.6-1.7-1.1-.5-.5-.9-1-1.1-1.7-.3-.7-.4-1.4-.5-2.5C2 15.1 2 14.7 2 12s0-3.1.1-4.1c0-1.1.2-1.8.5-2.5.3-.7.6-1.2 1.1-1.7.5-.5 1-.9 1.7-1.1.7-.3 1.4-.4 2.5-.5C8.9 2 9.3 2 12 2Zm0 1.8c-2.6 0-3 0-4 .1-.9 0-1.4.2-1.7.3-.4.2-.7.3-1 .6-.3.3-.5.6-.6 1-.1.3-.3.8-.3 1.7-.1 1-.1 1.4-.1 4s0 3 .1 4c0 .9.2 1.4.3 1.7.2.4.3.7.6 1 .3.3.6.5 1 .6.3.1.8.3 1.7.3 1 .1 1.4.1 4 .1s3 0 4-.1c.9 0 1.4-.2 1.7-.3.4-.2.7-.3 1-.6.3-.3.5-.6.6-1 .1-.3.3-.8.3-1.7.1-1 .1-1.4.1-4s0-3-.1-4c0-.9-.2-1.4-.3-1.7-.2-.4-.3-.7-.6-1-.3-.3-.6-.5-1-.6-.3-.1-.8-.3-1.7-.3-1-.1-1.4-.1-4-.1Zm0 3.5a4.7 4.7 0 1 1 0 9.4 4.7 4.7 0 0 1 0-9.4Zm0 1.8a2.9 2.9 0 1 0 0 5.8 2.9 2.9 0 0 0 0-5.8Zm5-2a1.1 1.1 0 1 1-2.2 0 1.1 1.1 0 0 1 2.2 0Z"/></svg></a>
          <a href="https://twitter.com/RowanIEEE" target="_blank" rel="noopener" aria-label="X (Twitter)"><svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M18.9 2H22l-7.6 8.7L23.3 22h-7.2l-5.6-7.3L4 22H1l8.1-9.3L.9 2h7.4l5.1 6.7L18.9 2Zm-1.3 18h1.9L7.5 3.9H5.4L17.6 20Z"/></svg></a>
        </div>
      </div>
      <div>
        <h4>Explore</h4>
        <ul>
          <li><a href="about.html">About</a></li>
          <li><a href="events.html">Events</a></li>
          <li><a href="projects.html">Showcase</a></li>
          <li><a href="team.html">Team</a></li>
        </ul>
      </div>
      <div>
        <h4>Get involved</h4>
        <ul>
          <li><a href="contact.html">Contact the E-Board</a></li>
          <li><a href="https://discord.com/invite/ZesVYMSJWe" target="_blank" rel="noopener">Discord</a></li>
          <li><a href="https://profhacks.rowanieee.org" target="_blank" rel="noopener">ProfHacks 2026</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; <span id="year"></span> Rowan IEEE Student Branch. All rights reserved.</span>
      <span>IEEE Region 2 &middot; Rowan University, Glassboro, NJ</span>
    </div>
  </div>
</footer>

<script src="js/main.js"></script>
</body>
</html>
"""

PAGES = {}

# ---------------------------------------------------------------- ABOUT ----
PAGES["about.html"] = dict(
    title="About",
    desc="What is IEEE, and what does Rowan IEEE's Student Branch do? Meeting times, mission, and why to join.",
    main="""
<main>
  <section class="hero" style="padding-top:64px;padding-bottom:56px;">
    <div class="container">
      <span class="eyebrow">About us</span>
      <h1>So, what is <span>IEEE</span>?</h1>
      <p class="lead">IEEE, pronounced &ldquo;Eye-triple-E&rdquo;, stands for the Institute of Electrical and Electronics Engineers &mdash; and Rowan's student branch brings it to campus.</p>
    </div>
  </section>

  <section style="padding-top:0;">
    <div class="container">
      <div class="split">
        <div>
          <span class="kicker">Globally</span>
          <h2>The world's largest technical professional society</h2>
          <p>IEEE is an association dedicated to advancing innovation and technological excellence for the benefit of humanity. It's designed to serve professionals involved in all aspects of the electrical, electronic, and computing fields and related areas of science and technology that underlie modern civilization.</p>
        </div>
        <div>
          <span class="kicker">Right here</span>
          <h2>Rowan IEEE's Student Branch</h2>
          <p>Our branch is a University club, much like any other &mdash; part of IEEE Region 2. Students of all majors who want a fun, relaxed place to improve themselves professionally and technically are welcome, whether you're into circuits, code, or you just want to see what we're about.</p>
        </div>
      </div>
    </div>
  </section>

  <section>
    <div class="container">
      <div class="section-head">
        <span class="kicker">Meetings</span>
        <h2>When &amp; where we meet</h2>
        <div class="divider-rule"></div>
      </div>
      <div class="card-grid cols-2">
        <div class="card">
          <div class="icon-badge"><svg width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M7 3v4M17 3v4M3 9h18M5 6h14a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2Z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg></div>
          <h3>General meetings</h3>
          <p>Bi-weekly on Fridays at 2PM in Engineering 321. We recap upcoming events, then dive into a presentation, seminar, or guest speaker. Pizza and drinks are always provided.</p>
        </div>
        <div class="card">
          <div class="icon-badge"><svg width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M12 21s-7-4.4-9.5-8.7C.7 8.7 2.4 5 6 5c2 0 3.4 1 4 2.3.6-1.3 2-2.3 4-2.3 3.6 0 5.3 3.7 3.5 7.3C19 16.6 12 21 12 21Z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg></div>
          <h3>Everyone's welcome</h3>
          <p>No electrical engineering degree required. Computer science, mechanical, business, undecided &mdash; if you're curious and want a relaxed community, you're in the right place.</p>
        </div>
      </div>
    </div>
  </section>

  <section>
    <div class="container">
      <div class="cta-banner">
        <span class="kicker">Ready to check us out?</span>
        <h2>Come to a Friday meeting.</h2>
        <p>Engineering Hall, Room 321 &mdash; every other Friday at 2PM. Free pizza, no commitment required.</p>
        <div class="hero-actions">
          <a class="btn btn-primary" href="events.html">See the full event calendar</a>
          <a class="btn btn-ghost" href="team.html">Meet the E-Board</a>
        </div>
      </div>
    </div>
  </section>
</main>
""",
)

# --------------------------------------------------------------- EVENTS ----
PAGES["events.html"] = dict(
    title="Events",
    desc="General meetings, social activities, technical workshops, SAC 2026, and ProfHacks 2026: Space Cowboys.",
    main="""
<main>
  <section class="hero" style="padding-top:64px;padding-bottom:40px;">
    <div class="container">
      <span class="eyebrow">Calendar</span>
      <h1>Events &amp; <span>things to do</span></h1>
      <p class="lead">From our regular Friday meetings to a 24-hour hackathon, here's everything Rowan IEEE runs throughout the year.</p>
    </div>
  </section>

  <section style="padding-top:0;">
    <div class="container">
      <div class="spotlight" style="margin-bottom:22px;">
        <div>
          <div class="badge-row">
            <span class="tag tag-gold">March 20&ndash;21, 2026</span>
            <span class="tag tag-blue">Rowan University, Glassboro NJ</span>
          </div>
          <h2>SAC 2026 &mdash; Student Activities Conference</h2>
          <p>A major professional conference for IEEE student members, featuring technical competitions like SumoBot, Arduino, and paper presentations, plus networking and corporate showcases.</p>
        </div>
        <img class="media-photo" src="images/events/workshop.jpg" alt="IEEE student workshop and competition" loading="lazy" decoding="async">
      </div>

      <div class="spotlight">
        <div>
          <div class="badge-row">
            <span class="tag tag-gold">March 20&ndash;21, 2026</span>
            <span class="tag tag-blue">Registration opening soon</span>
          </div>
          <h2>ProfHacks 2026: Space Cowboys</h2>
          <p>Rowan University's annual 24-hour hackathon. Join us for a weekend of building, coding, and prizes. Visit the ProfHacks site for details and follow our Instagram for registration updates.</p>
          <div class="hero-actions" style="justify-content:flex-start;margin-bottom:0;">
            <a class="btn btn-gold" href="https://profhacks.rowanieee.org" target="_blank" rel="noopener">Visit profhacks.rowanieee.org</a>
          </div>
        </div>
        <img class="media-photo" src="images/events/profhacks-2026.png" alt="ProfHacks 2026: Space Cowboys" loading="lazy" decoding="async">
      </div>
    </div>
  </section>

  <section>
    <div class="container">
      <div class="section-head">
        <span class="kicker">All year round</span>
        <h2>The regular lineup</h2>
        <div class="divider-rule"></div>
      </div>
      <div class="timeline">
        <div class="timeline-item">
          <h3>General meetings</h3>
          <div class="meta">Bi-weekly &middot; Fridays, 2PM &middot; Engineering 321</div>
          <p>Upcoming-event recaps followed by a short presentation, seminar, or guest speaker. Pizza and drinks provided.</p>
        </div>
        <div class="timeline-item">
          <h3>Technical workshops</h3>
          <div class="meta">Throughout the semester</div>
          <p>Hands-on sessions covering resume building, Git, Verilog, Arduino, PCB design, and more.</p>
        </div>
        <div class="timeline-item">
          <h3>Social activities</h3>
          <div class="meta">Throughout the semester &middot; Free for members</div>
          <p>Paintball, Top Golf, trampoline parks, and other outings the E-Board plans for the club.</p>
        </div>
      </div>
    </div>
  </section>

  <section>
    <div class="container">
      <div class="cta-banner">
        <span class="kicker">Don't miss out</span>
        <h2>Get event pings on Discord.</h2>
        <p>We post meeting reminders, workshop sign-ups, and hackathon updates there first.</p>
        <div class="hero-actions">
          <a class="btn btn-primary" href="https://discord.com/invite/ZesVYMSJWe" target="_blank" rel="noopener">Join our Discord</a>
        </div>
      </div>
    </div>
  </section>
</main>
""",
)

# ------------------------------------------------------------- PROJECTS ----
PAGES["projects.html"] = dict(
    title="Showcase",
    desc="What Rowan IEEE members build: competitions, technical workshops, and hackathon projects.",
    main="""
<main>
  <section class="hero" style="padding-top:64px;padding-bottom:40px;">
    <div class="container">
      <span class="eyebrow">Showcase</span>
      <h1>What our members <span>build</span></h1>
      <p class="lead">Competitions, workshops, and hackathon projects &mdash; this is where we show off what Rowan IEEE actually does. The E-Board is filling this page in with real photos and write-ups as they come in from each event.</p>
    </div>
  </section>

  <section style="padding-top:0;">
    <div class="container">
      <div class="section-head">
        <span class="kicker">Competitions</span>
        <h2>SAC &amp; robotics competitions</h2>
        <div class="divider-rule"></div>
      </div>
      <div class="card-grid cols-2">
        <div class="card">
          <img class="media-photo" style="margin-bottom:18px;" src="images/events/workshop.jpg" alt="SumoBot and robotics competition" loading="lazy" decoding="async">
          <span class="tag tag-blue">SAC Competition</span>
          <h3>SumoBot</h3>
          <p>Members design, build, and program small robots to compete head-to-head at the Student Activities Conference.</p>
        </div>
        <div class="card">
          <img class="media-photo" style="margin-bottom:18px;" src="images/events/general-meeting.jpg" alt="Arduino and embedded projects" loading="lazy" decoding="async">
          <span class="tag tag-blue">SAC Competition</span>
          <h3>Arduino</h3>
          <p>A hands-on microcontroller challenge testing what teams can build and program under a time limit.</p>
        </div>
      </div>
    </div>
  </section>

  <section>
    <div class="container">
      <div class="section-head">
        <span class="kicker">Technical workshops</span>
        <h2>Skills members walk away with</h2>
        <div class="divider-rule"></div>
      </div>
      <div class="card-grid">
        <div class="card">
          <span class="tag tag-teal">Workshop</span>
          <h3>PCB design</h3>
          <p>Learn to lay out and design your own circuit boards from scratch.</p>
        </div>
        <div class="card">
          <span class="tag tag-teal">Workshop</span>
          <h3>Verilog</h3>
          <p>An intro to hardware description languages and digital logic design.</p>
        </div>
        <div class="card">
          <span class="tag tag-teal">Workshop</span>
          <h3>Arduino</h3>
          <p>Build and program simple embedded projects with real hardware.</p>
        </div>
        <div class="card">
          <span class="tag tag-teal">Workshop</span>
          <h3>Git</h3>
          <p>Version control basics for working on code with a team.</p>
        </div>
        <div class="card">
          <span class="tag tag-teal">Workshop</span>
          <h3>Resume building</h3>
          <p>Get your resume ready for career fairs and internship season.</p>
        </div>
        <div class="card">
          <div class="icon-badge"><svg width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg></div>
          <h3>Suggest a workshop</h3>
          <p>Have a topic you want covered? Let the E-Board know on Discord or the contact page.</p>
        </div>
      </div>
    </div>
  </section>

  <section>
    <div class="container">
      <div class="section-head">
        <span class="kicker">Hackathon</span>
        <h2>ProfHacks builds</h2>
        <p>A look back at ProfHacks 2024 &mdash; photos from this and future hackathons will fill out this gallery as the E-Board adds them.</p>
        <div class="divider-rule"></div>
      </div>
      <div class="gallery-grid">
        <img src="images/showcase/ph1.jpg" alt="ProfHacks 2024" loading="lazy" decoding="async">
        <img src="images/showcase/ph2.jpg" alt="ProfHacks 2024" loading="lazy" decoding="async">
        <img src="images/showcase/ph3.jpg" alt="ProfHacks 2024" loading="lazy" decoding="async">
        <img src="images/showcase/ph4.jpg" alt="ProfHacks 2024" loading="lazy" decoding="async">
        <img src="images/showcase/ph5.jpg" alt="ProfHacks 2024" loading="lazy" decoding="async">
        <img src="images/showcase/ph6.jpg" alt="ProfHacks 2024" loading="lazy" decoding="async">
        <img src="images/showcase/ph7.jpg" alt="ProfHacks 2024" loading="lazy" decoding="async">
        <img src="images/showcase/ph8.jpg" alt="ProfHacks 2024" loading="lazy" decoding="async">
        <img src="images/showcase/ph9.jpg" alt="ProfHacks 2024" loading="lazy" decoding="async">
        <img src="images/showcase/ph10.jpg" alt="ProfHacks 2024" loading="lazy" decoding="async">
        <img src="images/showcase/ph11.jpg" alt="ProfHacks 2024" loading="lazy" decoding="async">
        <img src="images/showcase/ph12.jpg" alt="ProfHacks 2024" loading="lazy" decoding="async">
        <img src="images/showcase/ph13.jpg" alt="ProfHacks 2024" loading="lazy" decoding="async">
        <img src="images/showcase/ph14.jpg" alt="ProfHacks 2024" loading="lazy" decoding="async">
        <img src="images/showcase/ph15.jpg" alt="ProfHacks 2024" loading="lazy" decoding="async">
        <img src="images/showcase/ph16.jpg" alt="ProfHacks 2024" loading="lazy" decoding="async">
      </div>
    </div>
  </section>

  <section>
    <div class="container">
      <div class="cta-banner">
        <span class="kicker">Built something?</span>
        <h2>We want to feature it.</h2>
        <p>Send your project photos and a short write-up to the E-Board and we'll add it to this page.</p>
        <div class="hero-actions">
          <a class="btn btn-primary" href="contact.html">Contact the E-Board</a>
        </div>
      </div>
    </div>
  </section>
</main>
""",
)

# ---------------------------------------------------------------- TEAM ----
def person(name, role, email, photo):
    return f"""
        <div class="card person-card">
          <img class="avatar" src="images/team/{photo}" alt="{name}" loading="lazy" decoding="async">
          <h3>{name}</h3>
          <div class="role">{role}</div>
          <a class="email" href="mailto:{email}">{email}</a>
        </div>"""

TEAM = [
    ("Aidan", "Chair", "olough74@rowan.edu", "aidan.jpeg"),
    ("Elisabeth", "Vice Chair", "yapeli32@students.rowan.edu", "elisabeth.jpeg"),
    ("Erika", "Treasurer", "rivera218@rowan.edu", "erika.jpeg"),
    ("Noelle", "Secretary", "rossno75@students.rowan.edu", "noelle.jpeg"),
    ("Duru", "Fundraising Chair", "yesily79@rowan.edu", "duru.jpeg"),
    ("Kadin", "Webmaster", "Bevank82@rowan.edu", "kadin.jpeg"),
    ("Maria", "Tournament Chair", "maione15@rowan.edu", "maria.jpeg"),
]

PAGES["team.html"] = dict(
    title="Team",
    desc="Meet the Rowan IEEE E-Board — Chair, Vice Chair, Treasurer, Secretary, Fundraising Chair, Webmaster, and Tournament Chair.",
    main=f"""
<main>
  <section class="hero" style="padding-top:64px;padding-bottom:40px;">
    <div class="container">
      <span class="eyebrow">Leadership</span>
      <h1>Meet the <span>E-Board</span></h1>
      <p class="lead">Seven students running events, workshops, and everything else that makes Rowan IEEE work. Reach out to any of us any time.</p>
    </div>
  </section>

  <section style="padding-top:0;">
    <div class="container">
      <div class="card-grid cols-4">{''.join(person(*p) for p in TEAM)}
        <div class="card">
          <span class="index-num">+1</span>
          <h3>ProfHacks committee</h3>
          <p>A big thanks to the ProfHacks committee for all of their hard work putting the hackathon together each year.</p>
        </div>
      </div>
    </div>
  </section>

  <section>
    <div class="container">
      <div class="cta-banner">
        <span class="kicker">Want to run for E-Board?</span>
        <h2>Get involved with leadership.</h2>
        <p>Come to a meeting, get to know the club, and ask any current E-Board member how elections work.</p>
        <div class="hero-actions">
          <a class="btn btn-primary" href="contact.html">Contact us</a>
        </div>
      </div>
    </div>
  </section>
</main>
""",
)

# -------------------------------------------------------------- CONTACT ----
PAGES["contact.html"] = dict(
    title="Contact",
    desc="Get in touch with Rowan IEEE — meeting location, Discord, Instagram, X, and a contact form.",
    main="""
<main>
  <section class="hero" style="padding-top:64px;padding-bottom:40px;">
    <div class="container">
      <span class="eyebrow">Say hello</span>
      <h1>Get in <span>touch</span></h1>
      <p class="lead">Questions about meetings, workshops, or joining? Reach out below or drop by a Friday meeting in person.</p>
    </div>
  </section>

  <section style="padding-top:0;">
    <div class="container">
      <div class="split">
        <div class="form-card">
          <h3 style="margin-bottom:18px;">Send us a message</h3>
          <form id="contact-form">
            <div class="field">
              <label for="name">Name</label>
              <input type="text" id="name" name="name" required>
            </div>
            <div class="field">
              <label for="email">Email</label>
              <input type="email" id="email" name="email" required>
            </div>
            <div class="field">
              <label for="message">Message</label>
              <textarea id="message" name="message" rows="5" required></textarea>
            </div>
            <button type="submit" class="btn btn-primary" style="width:100%;justify-content:center;">Send</button>
            <div id="form-status"></div>
          </form>
        </div>

        <div>
          <div class="info-card">
            <div class="icon-badge"><svg width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M12 21s6-6.4 6-11a6 6 0 1 0-12 0c0 4.6 6 11 6 11Z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><circle cx="12" cy="10" r="2.4" stroke="currentColor" stroke-width="1.6"/></svg></div>
            <div>
              <h3>General meetings</h3>
              <p>Engineering Hall, Room 321 &middot; bi-weekly Fridays, 2PM. Free pizza and drinks.</p>
            </div>
          </div>
          <div class="info-card">
            <div class="icon-badge"><svg width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M20.3 4.9A19.8 19.8 0 0 0 15.6 3.3c-.2.4-.5 1-.7 1.4a18.3 18.3 0 0 0-5.8 0c-.2-.5-.4-1-.7-1.4A19.7 19.7 0 0 0 3.7 4.9C1 8.9.3 12.8.6 16.7a19.9 19.9 0 0 0 6 3c.5-.6.9-1.3 1.3-2a13 13 0 0 1-2-1c.2-.1.3-.3.5-.4a14.2 14.2 0 0 0 12.2 0l.4.4c-.6.4-1.3.7-2 1 .4.7.8 1.4 1.3 2a19.8 19.8 0 0 0 6-3c.4-4.5-.7-8.4-3-11.8ZM8.8 14.3c-1 0-1.8-.9-1.8-2s.8-2 1.8-2 1.8.9 1.8 2-.8 2-1.8 2Zm6.4 0c-1 0-1.8-.9-1.8-2s.8-2 1.8-2 1.8.9 1.8 2-.8 2-1.8 2Z" fill="currentColor" stroke="none"/></svg></div>
            <div>
              <h3>Discord</h3>
              <p>The fastest way to reach us &mdash; <a href="https://discord.com/invite/ZesVYMSJWe" target="_blank" rel="noopener" style="color:var(--blue-300);">join the server</a>.</p>
            </div>
          </div>
          <div class="info-card">
            <div class="icon-badge"><svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2c2.7 0 3.1 0 4.1.1 1.1 0 1.8.2 2.5.5.7.3 1.2.6 1.7 1.1.5.5.9 1 1.1 1.7.3.7.4 1.4.5 2.5 0 1 .1 1.4.1 4.1s0 3.1-.1 4.1c0 1.1-.2 1.8-.5 2.5-.3.7-.6 1.2-1.1 1.7-.5.5-1 .9-1.7 1.1-.7.3-1.4.4-2.5.5-1 0-1.4.1-4.1.1s-3.1 0-4.1-.1c-1.1 0-1.8-.2-2.5-.5-.7-.3-1.2-.6-1.7-1.1-.5-.5-.9-1-1.1-1.7-.3-.7-.4-1.4-.5-2.5C2 15.1 2 14.7 2 12s0-3.1.1-4.1c0-1.1.2-1.8.5-2.5.3-.7.6-1.2 1.1-1.7.5-.5 1-.9 1.7-1.1.7-.3 1.4-.4 2.5-.5C8.9 2 9.3 2 12 2Zm0 1.8c-2.6 0-3 0-4 .1-.9 0-1.4.2-1.7.3-.4.2-.7.3-1 .6-.3.3-.5.6-.6 1-.1.3-.3.8-.3 1.7-.1 1-.1 1.4-.1 4s0 3 .1 4c0 .9.2 1.4.3 1.7.2.4.3.7.6 1 .3.3.6.5 1 .6.3.1.8.3 1.7.3 1 .1 1.4.1 4 .1s3 0 4-.1c.9 0 1.4-.2 1.7-.3.4-.2.7-.3 1-.6.3-.3.5-.6.6-1 .1-.3.3-.8.3-1.7.1-1 .1-1.4.1-4s0-3-.1-4c0-.9-.2-1.4-.3-1.7-.2-.4-.3-.7-.6-1-.3-.3-.6-.5-1-.6-.3-.1-.8-.3-1.7-.3-1-.1-1.4-.1-4-.1Zm0 3.5a4.7 4.7 0 1 1 0 9.4 4.7 4.7 0 0 1 0-9.4Zm0 1.8a2.9 2.9 0 1 0 0 5.8 2.9 2.9 0 0 0 0-5.8Zm5-2a1.1 1.1 0 1 1-2.2 0 1.1 1.1 0 0 1 2.2 0Z"/></svg></div>
            <div>
              <h3>Instagram &amp; X</h3>
              <p><a href="https://www.instagram.com/rowanieee/" target="_blank" rel="noopener" style="color:var(--blue-300);">@rowanieee</a> &middot; <a href="https://twitter.com/RowanIEEE" target="_blank" rel="noopener" style="color:var(--blue-300);">@RowanIEEE</a></p>
            </div>
          </div>
          <div class="info-card">
            <div class="icon-badge"><svg width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M4 4h16v12H7l-3 3V4Z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg></div>
            <div>
              <h3>E-Board emails</h3>
              <p>Prefer email? Find every officer's address on the <a href="team.html" style="color:var(--blue-300);">Team page</a>.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</main>
""",
)

os.chdir(os.path.dirname(os.path.abspath(__file__)))
EMAILJS_SCRIPTS = """<script src="https://cdn.jsdelivr.net/npm/@emailjs/browser@4/dist/email.min.js"></script>
<script>
  emailjs.init("orwF1ZJV_UumtHVN3");
</script>
<script src="js/main.js"></script>"""

for filename, page in PAGES.items():
    footer = FOOTER
    if filename == "contact.html":
        footer = FOOTER.replace('<script src="js/main.js"></script>', EMAILJS_SCRIPTS)
    html = HEAD.format(title=page["title"], desc=page["desc"]) + HEADER + page["main"] + footer
    with open(filename, "w") as f:
        f.write(html)
    print("wrote", filename)
