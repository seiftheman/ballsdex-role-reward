(() => {
  const root = document.documentElement;
  const sections = [...document.querySelectorAll(".reveal-section")];

  root.classList.add("js");

  if (!sections.length) {
    return;
  }

  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (reduced || !("IntersectionObserver" in window)) {
    sections.forEach((section) => section.classList.add("active"));
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("active");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: "0px 0px -8% 0px" }
  );

  sections.forEach((section) => observer.observe(section));
})();
