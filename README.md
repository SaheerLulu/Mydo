# Biloop — Industry Transformation Campaign

A complete, ready-to-publish content package on **how AI (Biloop) transforms five industries**:

- 💊 **Pharmacy Retail**
- 📊 **Accounting**
- 🏢 **Real Estate**
- 🛠️ **AMC & Field Service**
- 🛢️ **Oil & Gas**

It contains **10 LinkedIn posts** (2 per industry) and **5 detailed blog articles** published as a **GitHub Pages** website.

## What's in this repo

```
.
├── index.html                 # Landing page (links to all blogs + posts)
├── assets/css/style.css       # Shared site styling
├── blogs/                     # 5 detailed industry deep-dives (HTML)
│   ├── pharmacy-retail.html
│   ├── accounting.html
│   ├── real-estate.html
│   ├── amc.html
│   └── oil-and-gas.html
├── linkedin-posts/            # 10 LinkedIn posts + posting guide
│   ├── README.md              # Index, posting plan & tips
│   └── 01..10-*.md            # One file per post
├── .github/workflows/pages.yml  # Auto-deploy to GitHub Pages
└── .nojekyll                  # Serve static HTML as-is (no Jekyll build)
```

## Publishing to GitHub Pages

> ⚠️ **GitHub Pages must be turned on once, by hand, in repo Settings.**
> Automated deploys cannot do this: GitHub blocks the Actions token from
> creating the Pages site (`Resource not accessible by integration`). This is a
> one-time switch only a repo admin can flip — after that the site stays live.

The site is plain static HTML, so no build step is needed.

### ✅ Option A — Deploy from a branch (simplest — do this)
1. Open **Settings → Pages**.
2. Under **Build and deployment → Source**, pick **Deploy from a branch**.
3. **Branch:** select `claude/linkedin-posts-github-blogs-12AuF` (or `main` after merging) · **Folder:** `/ (root)`.
4. Click **Save**. Wait ~1 minute and refresh — the live URL appears at the top of the same page.

This bypasses the workflow entirely and just serves the files. Nothing else to do.

### Option B — GitHub Actions source
1. **Settings → Pages → Source → GitHub Actions**.
2. Run the workflow manually: **Actions → Deploy to GitHub Pages → Run workflow**.

Once live, the site is available at:

```
https://saheerlulu.github.io/mydo/
```

(blogs at `https://saheerlulu.github.io/mydo/blogs/<name>.html`)

## Using the LinkedIn posts

Open [`linkedin-posts/README.md`](linkedin-posts/README.md) for the full posting plan and tips. Before posting, replace each `[link to blog]` placeholder with the live GitHub Pages URL of the matching deep-dive.

---

© 2026 Biloop. AI that transforms how industries work. · [biloop.ai](https://biloop.ai) · info@biloop.ai
