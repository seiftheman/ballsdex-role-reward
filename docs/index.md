---
hide:
  - navigation
  - toc
---

<div class="home-page">

  <section class="hero reveal-section">
    <div class="hero-grid">
      <div class="hero-copy">
        <p class="hero-eyebrow reveal-item">BallsDex 3.0+ · Django admin</p>
        <h1 class="reveal-item">Roles worth<br><span class="gradient-text">earning.</span></h1>
        <p class="hero-lede reveal-item">
          A progression-based role reward package for BallsDex. Set a collection
          threshold in the Django admin and let the bot <strong>grant a role
          automatically</strong> every five minutes.
        </p>
        <div class="hero-actions reveal-item">
          <a class="md-button md-button--primary" href="installation/">Install v1.3.0</a>
          <a class="md-button" href="https://github.com/seiftheman/ballsdex-role-reward/releases">View releases</a>
        </div>
        <div class="hero-stats reveal-item">
          <div class="hero-stat"><strong>5 min</strong><span>Check interval</span></div>
          <div class="hero-stat"><strong>1 row</strong><span>Admin settings</span></div>
          <div class="hero-stat"><strong>v1.3.0</strong><span>Current release</span></div>
        </div>
      </div>

      <div class="shop-scene" aria-hidden="true">
        <div class="floating-tag one">Live settings reload</div>
        <div class="shop-preview">
          <div class="shop-topline">
            <div class="shop-label"><img src="assets/logo-256.png" alt="">Reward settings</div>
            <span class="live-badge">Active</span>
          </div>
          <div class="shop-card">
            <div class="shop-eyebrow">Eligible now</div>
            <h3>Collection milestone</h3>
            <p>1% of enabled balls unlocks the access role.</p>
            <div class="shop-row"><span>Enabled balls</span><span>240</span></div>
            <div class="shop-row"><span>Required progression</span><span class="price">1.00%</span></div>
            <div class="shop-row"><span>Target</span><span>3/240 distinct</span></div>
            <div class="shop-row"><span>Already rewarded</span><span>12 members</span></div>
            <div class="stock-meter"><span></span></div>
            <div class="stock-note"><span>12 of 18 rewarded</span><span>67%</span></div>
          </div>
          <div class="shop-actions">
            <div class="shop-button ghost">Server</div>
            <div class="shop-button buy">Run check</div>
            <div class="shop-button ghost">Role</div>
          </div>
        </div>
        <div class="floating-tag two">5-minute checks</div>
      </div>
    </div>

    <div class="scroll-cue" aria-hidden="true">
      <span>Scroll to explore</span>
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4v14m-6-6 6 6 6-6"/></svg>
    </div>
  </section>

  <div class="feature-strip reveal-section">
    <span>Admin settings</span>
    <span>Live reload</span>
    <span>Automatic checks</span>
    <span>Role validation</span>
    <span>Owner command</span>
    <span>Django backed</span>
  </div>

  <section class="home-section reveal-section">
    <p class="section-kicker reveal-item">Feature set</p>
    <h2 class="reveal-item">Rewards that manage themselves.</h2>
    <p class="section-lede reveal-item">Configure one settings row, choose a collection threshold, and let the package handle the rest without restarting the bot.</p>

    <div class="feature-grid">
      <article class="feature-card reveal-item">
        <div class="feature-icon" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6h16M4 12h16M4 18h16"/><circle cx="8" cy="6" r="2" fill="currentColor" stroke="none"/><circle cx="16" cy="12" r="2" fill="currentColor" stroke="none"/><circle cx="10" cy="18" r="2" fill="currentColor" stroke="none"/></svg>
        </div>
        <h3>Simple admin configuration</h3>
        <p>One <strong>Role reward settings</strong> row holds the server, reward role, and progression fraction. No separate config file is needed.</p>
        <span class="card-tag">One settings row</span>
      </article>

      <article class="feature-card reveal-item">
        <div class="feature-icon" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 11a8 8 0 1 0-2.3 5.7"/><path d="M20 4v7h-7"/></svg>
        </div>
        <h3>Live settings reload</h3>
        <p>Saving or deleting the settings row updates the running check immediately through Django signals.</p>
        <span class="card-tag">No restart needed</span>
      </article>

      <article class="feature-card reveal-item">
        <div class="feature-icon" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>
        </div>
        <h3>Automatic checks</h3>
        <p>Every five minutes the cog recalculates eligibility and grants the reward role to qualifying players.</p>
        <span class="card-tag">Every 5 minutes</span>
      </article>

      <article class="feature-card reveal-item">
        <div class="feature-icon" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3 4.5 6v5.5c0 4.7 3.2 8.1 7.5 9.5 4.3-1.4 7.5-4.8 7.5-9.5V6L12 3Z"/><path d="m9 12 2 2 4-4"/></svg>
        </div>
        <h3>Safe role validation</h3>
        <p>Before assigning anything, the bot checks permissions, role hierarchy, and whether the role is managed or <code>@everyone</code>.</p>
        <span class="card-tag">Permission aware</span>
      </article>

      <article class="feature-card reveal-item">
        <div class="feature-icon" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19V9m5 10V5m5 14v-7m5 7V8"/></svg>
        </div>
        <h3>Clear progress maths</h3>
        <p>Eligibility uses distinct enabled balls and rounds the target up, so even a small percentage requires at least one ball.</p>
        <span class="card-tag">Ceiled target</span>
      </article>

      <article class="feature-card reveal-item">
        <div class="feature-icon" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3 2.2 6.8H21l-5.5 4 2.1 6.7-5.6-4.1L6.4 20.5l2.1-6.7-5.5-4h6.8L12 3Z"/></svg>
        </div>
        <h3>Owner-only manual check</h3>
        <p>Run <code>rolereward</code> in the configured server for an immediate report. The old <code>hello</code> alias is kept for compatibility.</p>
        <span class="card-tag">Detailed counters</span>
      </article>
    </div>

    <div class="release-band reveal-item">
      <div>
        <h3>New in v1.3.0</h3>
        <p>Stronger settings validation, safer reward checks, and a full test suite.</p>
      </div>
      <a class="md-button" href="https://github.com/seiftheman/ballsdex-role-reward/releases/tag/v1.3.0">Read release notes</a>
    </div>
  </section>

</div>

<div class="home-section home-quickstart reveal-section" markdown>

## Quick start { .reveal-item }

Add the package to your BallsDex `config/extra.toml`:

```toml
[[ballsdex.packages]]
location = "git+https://github.com/seiftheman/ballsdex-role-reward.git@v1.3.0#main"
path = "role_reward"
enabled = true
```

Restart the bot once so Django applies the package migrations. Then open the Django
admin panel and create a single **Role reward settings** row.

[Installation guide](installation.md){ .md-button .md-button--primary }
[Command reference](commands.md){ .md-button }
[Configuration](configuration.md){ .md-button }

</div>
