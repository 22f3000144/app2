<template>
  <div class="company-home-page">

    <!-- Hero Section -->
    <section class="hero-section">

      <div class="hero-content">

        <span class="hero-badge">
          Placement Recruitment Platform
        </span>

        <h1>
          Connect With
          <span>Top Talent</span>
          Across Campuses
        </h1>

        <p>
          Create placement drives, shortlist skilled students,
          schedule interviews, and streamline hiring with a
          modern campus recruitment platform.
        </p>

        <div class="hero-buttons">

          <router-link
            to="/company/dashboard"
            class="primary-btn"
          >
            Go To Dashboard
          </router-link>

          <router-link
            to="/company/register"
            class="secondary-btn"
          >
            Register Company
          </router-link>

        </div>

      </div>

      <div class="hero-image">

        <div class="floating-card purple-card">
          <h3>2500+</h3>
          <p>Student Applications</p>
        </div>

        <div class="floating-card red-card">
          <h3>120+</h3>
          <p>Placement Drives</p>
        </div>

        <div class="main-circle"></div>

      </div>

    </section>

    <!-- Features -->
    <section class="features-section">

      <div class="section-header">

        <h2>Why Companies Prefer Our Platform</h2>

        <p>
          Simplified hiring experience designed for modern
          campus recruitment.
        </p>

      </div>

      <div class="feature-grid">

        <div class="feature-card">

          <div class="icon purple-bg">
            📄
          </div>

          <h3>Create Drives</h3>

          <p>
            Post placement opportunities with eligibility,
            CGPA criteria, and deadlines in minutes.
          </p>

        </div>

        <div class="feature-card">

          <div class="icon red-bg">
            👨‍🎓
          </div>

          <h3>Manage Applicants</h3>

          <p>
            View applications, shortlist students,
            and manage recruitment pipelines efficiently.
          </p>

        </div>

        <div class="feature-card">

          <div class="icon purple-bg">
            📅
          </div>

          <h3>Schedule Interviews</h3>

          <p>
            Organize interview rounds with date scheduling
            and candidate status tracking.
          </p>

        </div>

        <div class="feature-card">

          <div class="icon red-bg">
            📊
          </div>

          <h3>Analytics Dashboard</h3>

          <p>
            Track drives, applications, and selections
            with clean dashboard insights.
          </p>

        </div>

      </div>

    </section>

    <!-- Stats -->
    <section class="stats-section">

      <div class="stats-card">

        <h2>500+</h2>
        <p>Partner Companies</p>

      </div>

      <div class="stats-card">

        <h2>20K+</h2>
        <p>Registered Students</p>

      </div>

      <div class="stats-card">

        <h2>95%</h2>
        <p>Placement Success</p>

      </div>

      <div class="stats-card">

        <h2>24/7</h2>
        <p>Recruitment Access</p>

      </div>

    </section>

    <!-- CTA -->
    <section class="cta-section">

      <div class="cta-content">

        <h2>
          Start Hiring Smarter Today
        </h2>

        <p>
          Join the platform and recruit the best talent
          from leading campuses.
        </p>

        <router-link
          to="/company/register"
          class="cta-btn"
        >
          Get Started
        </router-link>

      </div>

    </section>

  </div>
</template>

<script>
export default {

  name: "CompanyHomeView"

};
</script>

<style scoped>

.company-home-page {

  background: #fff;
  min-height: 100vh;
  overflow-x: hidden;

}

/* =========================
   HERO
========================= */

.hero-section {

  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 80px 8%;
  gap: 60px;
  min-height: 100vh;
  background:
    linear-gradient(
      135deg,
      #fff5f8,
      #f6f0ff
    );

}

.hero-content {

  flex: 1;

}

.hero-badge {

  display: inline-block;
  background: rgba(124, 58, 237, 0.1);
  color: #7c3aed;
  padding: 10px 18px;
  border-radius: 40px;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 24px;

}

.hero-content h1 {

  font-size: 64px;
  line-height: 1.1;
  margin-bottom: 24px;
  color: #1e1b4b;

}

.hero-content h1 span {

  color: #dc2626;

}

.hero-content p {

  font-size: 18px;
  line-height: 1.8;
  color: #64748b;
  max-width: 650px;
  margin-bottom: 36px;

}

.hero-buttons {

  display: flex;
  gap: 18px;
  flex-wrap: wrap;

}

.primary-btn,
.secondary-btn,
.cta-btn {

  text-decoration: none;
  padding: 14px 28px;
  border-radius: 14px;
  font-weight: 700;
  transition: 0.3s;

}

.primary-btn {

  background:
    linear-gradient(
      135deg,
      #7c3aed,
      #dc2626
    );

  color: white;

}

.primary-btn:hover {

  transform: translateY(-2px);

}

.secondary-btn {

  border: 2px solid #7c3aed;
  color: #7c3aed;

}

.secondary-btn:hover {

  background: #7c3aed;
  color: white;

}

/* =========================
   HERO IMAGE
========================= */

.hero-image {

  flex: 1;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;

}

.main-circle {

  width: 420px;
  height: 420px;

  background:
    linear-gradient(
      135deg,
      #7c3aed,
      #dc2626
    );

  border-radius: 50%;

  box-shadow:
    0 30px 60px rgba(124, 58, 237, 0.3);

}

.floating-card {

  position: absolute;
  background: white;
  padding: 22px;
  border-radius: 18px;
  min-width: 200px;
  box-shadow:
    0 15px 40px rgba(0,0,0,0.08);

}

.floating-card h3 {

  margin: 0;
  font-size: 32px;

}

.floating-card p {

  margin-top: 8px;
  color: #64748b;

}

.purple-card {

  top: 80px;
  left: 0;

}

.purple-card h3 {

  color: #7c3aed;

}

.red-card {

  bottom: 60px;
  right: 0;

}

.red-card h3 {

  color: #dc2626;

}

/* =========================
   FEATURES
========================= */

.features-section {

  padding: 100px 8%;
  background: white;

}

.section-header {

  text-align: center;
  margin-bottom: 60px;

}

.section-header h2 {

  font-size: 42px;
  color: #1e1b4b;
  margin-bottom: 14px;

}

.section-header p {

  color: #64748b;
  font-size: 17px;

}

.feature-grid {

  display: grid;
  grid-template-columns:
    repeat(auto-fit, minmax(260px, 1fr));

  gap: 28px;

}

.feature-card {

  background: white;
  border-radius: 24px;
  padding: 32px;
  border: 1px solid #f1f5f9;
  transition: 0.3s;

  box-shadow:
    0 10px 30px rgba(0,0,0,0.04);

}

.feature-card:hover {

  transform: translateY(-8px);

}

.icon {

  width: 70px;
  height: 70px;
  border-radius: 20px;

  display: flex;
  align-items: center;
  justify-content: center;

  font-size: 30px;
  margin-bottom: 24px;

}

.purple-bg {

  background: rgba(124, 58, 237, 0.12);

}

.red-bg {

  background: rgba(220, 38, 38, 0.12);

}

.feature-card h3 {

  margin-bottom: 14px;
  color: #1e1b4b;

}

.feature-card p {

  line-height: 1.8;
  color: #64748b;

}

/* =========================
   STATS
========================= */

.stats-section {

  padding: 60px 8%;
  display: grid;

  grid-template-columns:
    repeat(auto-fit, minmax(220px, 1fr));

  gap: 24px;

  background:
    linear-gradient(
      135deg,
      #7c3aed,
      #dc2626
    );

}

.stats-card {

  background: rgba(255,255,255,0.12);
  backdrop-filter: blur(10px);

  border-radius: 22px;
  padding: 32px;
  text-align: center;
  color: white;

}

.stats-card h2 {

  font-size: 42px;
  margin-bottom: 10px;

}

/* =========================
   CTA
========================= */

.cta-section {

  padding: 100px 8%;
  text-align: center;
  background: #fff7fb;

}

.cta-content h2 {

  font-size: 48px;
  margin-bottom: 18px;
  color: #1e1b4b;

}

.cta-content p {

  color: #64748b;
  font-size: 18px;
  margin-bottom: 36px;

}

.cta-btn {

  background:
    linear-gradient(
      135deg,
      #7c3aed,
      #dc2626
    );

  color: white;
  display: inline-block;

}

/* =========================
   RESPONSIVE
========================= */

@media (max-width: 992px) {

  .hero-section {

    flex-direction: column;
    text-align: center;
    padding-top: 120px;

  }

  .hero-buttons {

    justify-content: center;

  }

  .hero-content h1 {

    font-size: 48px;

  }

}

@media (max-width: 768px) {

  .hero-content h1 {

    font-size: 38px;

  }

  .section-header h2,
  .cta-content h2 {

    font-size: 32px;

  }

  .main-circle {

    width: 300px;
    height: 300px;

  }

  .floating-card {

    position: static;
    margin: 12px;

  }

  .hero-image {

    flex-direction: column;

  }

}

</style>