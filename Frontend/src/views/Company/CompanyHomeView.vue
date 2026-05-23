<template>
  <div class="company-home-page">

    <!-- HERO SECTION -->
    <section class="hero-section">

      <div class="container">

        <div class="row align-items-center min-vh-75">

          <!-- LEFT -->
          <div class="col-lg-6">

            <div class="hero-content">

              <span class="hero-badge">
                Placement Portal Platform
              </span>

              <h1 class="hero-title">
                Hire Skilled Students
                <span>From Top Institutes</span>
              </h1>

              <p class="hero-description">
                Create placement drives, manage applications,
                shortlist talented candidates, and streamline
                your campus recruitment process through one
                unified platform.
              </p>

              <div class="hero-buttons">

                <router-link
                  to="/company/register"
                  class="btn btn-primary btn-lg"
                >
                  Register Company
                </router-link>

                <router-link
                  to="/login"
                  class="btn btn-outline-light btn-lg"
                >
                  Company Login
                </router-link>

              </div>

            </div>

          </div>

          <!-- RIGHT -->
          <div class="col-lg-6">

            <div class="hero-image-wrapper">

              <div class="dashboard-card">

                <div class="dashboard-header">
                  <div class="circle red"></div>
                  <div class="circle yellow"></div>
                  <div class="circle green"></div>
                </div>

                <div class="dashboard-body">

                  <div class="stats-grid">

                    <div class="stat-card">
                      <h3>120+</h3>
                      <p>Placement Drives</p>
                    </div>

                    <div class="stat-card">
                      <h3>5K+</h3>
                      <p>Student Applications</p>
                    </div>

                    <div class="stat-card">
                      <h3>350+</h3>
                      <p>Companies</p>
                    </div>

                    <div class="stat-card">
                      <h3>92%</h3>
                      <p>Hiring Success</p>
                    </div>

                  </div>

                </div>

              </div>

            </div>

          </div>

        </div>

      </div>

    </section>

    <!-- FEATURES -->
    <section class="features-section">

      <div class="container">

        <div class="section-header text-center">

          <h2>
            Everything Your Recruitment Team Needs
          </h2>

          <p>
            Built according to modern placement workflow requirements
          </p>

        </div>

        <div class="row g-4 mt-4">

          <div
            class="col-md-6 col-lg-3"
            v-for="feature in features"
            :key="feature.title"
          >

            <div class="feature-card">

              <div class="feature-icon">
                <i :class="feature.icon"></i>
              </div>

              <h4>{{ feature.title }}</h4>

              <p>{{ feature.description }}</p>

            </div>

          </div>

        </div>

      </div>

    </section>

    <!-- WORKFLOW -->
    <section class="workflow-section">

      <div class="container">

        <div class="section-header text-center">

          <h2>
            Recruitment Workflow
          </h2>

          <p>
            Simple and structured hiring process
          </p>

        </div>

        <div class="row mt-5">

          <div
            class="col-md-3"
            v-for="(step, index) in workflow"
            :key="step.title"
          >

            <div class="workflow-card">

              <div class="step-number">
                {{ index + 1 }}
              </div>

              <h5>{{ step.title }}</h5>

              <p>{{ step.description }}</p>

            </div>

          </div>

        </div>

      </div>

    </section>

    <!-- BENEFITS -->
    <section class="benefits-section">

      <div class="container">

        <div class="row align-items-center">

          <div class="col-lg-6">

            <div class="benefits-content">

              <h2>
                Why Companies Prefer Our Portal
              </h2>

              <p class="benefit-intro">
                Designed for efficient placement management
                and seamless student recruitment.
              </p>

              <div class="benefit-list">

                <div
                  class="benefit-item"
                  v-for="benefit in benefits"
                  :key="benefit"
                >

                  <i class="bi bi-check-circle-fill"></i>

                  <span>{{ benefit }}</span>

                </div>

              </div>

            </div>

          </div>

          <div class="col-lg-6">

            <div class="benefit-image">

              <div class="floating-card top-card">
                <h4>Drive Approval</h4>
                <p>Admin verified placement process</p>
              </div>

              <div class="floating-card middle-card">
                <h4>Application Tracking</h4>
                <p>Monitor every student application</p>
              </div>

              <div class="floating-card bottom-card">
                <h4>Selection Updates</h4>
                <p>Update shortlisted & selected candidates</p>
              </div>

            </div>

          </div>

        </div>

      </div>

    </section>

    <!-- CTA -->
    <section class="cta-section">

      <div class="container">

        <div class="cta-card text-center">

          <h2>
            Start Your Campus Hiring Journey
          </h2>

          <p>
            Register your company profile and create placement drives today.
          </p>

          <router-link
            to="/company/register"
            class="btn btn-light btn-lg mt-3"
          >
            Get Started
          </router-link>

        </div>

      </div>

    </section>

  </div>
</template>

<script>
export default {

  name: "CompanyHomeView",

  data() {

    return {

      features: [
        {
          title: "Placement Drives",
          description:
            "Create and manage recruitment drives with eligibility rules.",
          icon: "bi bi-briefcase-fill"
        },
        {
          title: "Application Tracking",
          description:
            "Track student applications and manage hiring workflow.",
          icon: "bi bi-people-fill"
        },
        {
          title: "Shortlisting",
          description:
            "Shortlist qualified students and schedule interviews.",
          icon: "bi bi-person-check-fill"
        },
        {
          title: "Selection Updates",
          description:
            "Update application status dynamically for transparency.",
          icon: "bi bi-clipboard-check-fill"
        }
      ],

      workflow: [
        {
          title: "Register Company",
          description:
            "Create your company profile and wait for admin approval."
        },
        {
          title: "Create Drive",
          description:
            "Post placement drives with job roles and eligibility."
        },
        {
          title: "Review Applications",
          description:
            "View student applications and shortlist candidates."
        },
        {
          title: "Hire Students",
          description:
            "Conduct interviews and finalize student selections."
        }
      ],

      benefits: [
        "Centralized placement management",
        "Fast application handling",
        "Student eligibility filtering",
        "Real-time application updates",
        "Secure authentication system",
        "Streamlined recruitment workflow"
      ]

    }

  }

}
</script>

<style scoped>

/* =========================
   GLOBAL
========================= */

.company-home-page {
  background: #f5f7fb;
  overflow-x: hidden;
}

.min-vh-75 {
  min-height: 75vh;
}

.section-header h2 {
  font-size: 2.3rem;
  font-weight: 700;
  color: #0f172a;
}

.section-header p {
  color: #64748b;
  margin-top: 10px;
  font-size: 1rem;
}

/* =========================
   HERO SECTION
========================= */

.hero-section {
  background:
    linear-gradient(
      135deg,
      #0f172a,
      #1e293b,
      #2563eb
    );
  color: white;
  padding: 70px 0;
}

.hero-badge {
  background: rgba(255,255,255,0.15);
  padding: 10px 18px;
  border-radius: 50px;
  display: inline-block;
  margin-bottom: 20px;
  font-size: 0.9rem;
  font-weight: 600;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  line-height: 1.2;
}

.hero-title span {
  display: block;
  color: #93c5fd;
}

.hero-description {
  margin-top: 25px;
  color: #dbeafe;
  font-size: 1.1rem;
  line-height: 1.8;
  max-width: 550px;
}

.hero-buttons {
  margin-top: 35px;
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.hero-buttons .btn {
  padding: 14px 28px;
  font-weight: 600;
  border-radius: 12px;
}

/* =========================
   HERO CARD
========================= */

.hero-image-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 40px;
}

.dashboard-card {
  width: 100%;
  max-width: 520px;
  background: white;
  border-radius: 24px;
  overflow: hidden;
  box-shadow:
    0 20px 60px rgba(0,0,0,0.25);
}

.dashboard-header {
  background: #f1f5f9;
  padding: 15px;
  display: flex;
  gap: 10px;
}

.circle {
  width: 14px;
  height: 14px;
  border-radius: 50%;
}

.red {
  background: #ef4444;
}

.yellow {
  background: #f59e0b;
}

.green {
  background: #10b981;
}

.dashboard-body {
  padding: 30px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.stat-card {
  background: #f8fafc;
  border-radius: 18px;
  padding: 25px;
  text-align: center;
}

.stat-card h3 {
  font-size: 2rem;
  font-weight: 700;
  color: #2563eb;
}

.stat-card p {
  margin-top: 10px;
  color: #475569;
  font-size: 0.95rem;
}

/* =========================
   FEATURES
========================= */

.features-section {
  padding: 100px 0;
}

.feature-card {
  background: white;
  border-radius: 22px;
  padding: 35px 28px;
  height: 100%;
  transition: 0.3s ease;
  box-shadow:
    0 10px 30px rgba(0,0,0,0.05);
}

.feature-card:hover {
  transform: translateY(-8px);
}

.feature-icon {
  width: 70px;
  height: 70px;
  border-radius: 18px;
  background: #dbeafe;
  color: #2563eb;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
  margin-bottom: 20px;
}

.feature-card h4 {
  font-weight: 700;
  margin-bottom: 15px;
}

.feature-card p {
  color: #64748b;
  line-height: 1.7;
}

/* =========================
   WORKFLOW
========================= */

.workflow-section {
  padding: 100px 0;
  background: white;
}

.workflow-card {
  text-align: center;
  padding: 30px 20px;
}

.step-number {
  width: 70px;
  height: 70px;
  background: #2563eb;
  color: white;
  font-size: 1.6rem;
  font-weight: 700;
  border-radius: 50%;
  margin: auto;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.workflow-card h5 {
  font-weight: 700;
  margin-bottom: 15px;
}

.workflow-card p {
  color: #64748b;
  line-height: 1.7;
}

/* =========================
   BENEFITS
========================= */

.benefits-section {
  padding: 100px 0;
}

.benefits-content h2 {
  font-size: 2.5rem;
  font-weight: 700;
  color: #0f172a;
}

.benefit-intro {
  margin-top: 20px;
  color: #64748b;
  line-height: 1.8;
}

.benefit-list {
  margin-top: 30px;
}

.benefit-item {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 18px;
}

.benefit-item i {
  color: #10b981;
  font-size: 1.2rem;
}

.benefit-item span {
  color: #334155;
  font-weight: 500;
}

.benefit-image {
  position: relative;
  height: 420px;
}

.floating-card {
  position: absolute;
  background: white;
  padding: 28px;
  border-radius: 20px;
  width: 260px;
  box-shadow:
    0 15px 40px rgba(0,0,0,0.08);
}

.floating-card h4 {
  font-weight: 700;
}

.floating-card p {
  margin-top: 10px;
  color: #64748b;
}

.top-card {
  top: 0;
  left: 40px;
}

.middle-card {
  top: 140px;
  right: 0;
}

.bottom-card {
  bottom: 0;
  left: 80px;
}

/* =========================
   CTA
========================= */

.cta-section {
  padding: 100px 0;
}

.cta-card {
  background:
    linear-gradient(
      135deg,
      #2563eb,
      #1d4ed8
    );
  padding: 70px 40px;
  border-radius: 28px;
  color: white;
}

.cta-card h2 {
  font-size: 2.7rem;
  font-weight: 700;
}

.cta-card p {
  margin-top: 20px;
  color: #dbeafe;
  font-size: 1.1rem;
}

.cta-card .btn {
  padding: 14px 30px;
  border-radius: 12px;
  font-weight: 600;
}

/* =========================
   RESPONSIVE
========================= */

@media (max-width: 991px) {

  .hero-title {
    font-size: 2.7rem;
  }

  .benefit-image {
    margin-top: 50px;
    height: auto;
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .floating-card {
    position: static;
    width: 100%;
  }

}

@media (max-width: 768px) {

  .hero-section {
    text-align: center;
  }

  .hero-description {
    margin-left: auto;
    margin-right: auto;
  }

  .hero-buttons {
    justify-content: center;
  }

  .hero-title {
    font-size: 2.2rem;
  }

  .section-header h2,
  .benefits-content h2,
  .cta-card h2 {
    font-size: 2rem;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .cta-card {
    padding: 50px 25px;
  }

}

</style>