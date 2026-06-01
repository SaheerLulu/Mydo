# Mydo by Biloop — Industry Transformation Campaign

A complete, ready-to-publish content package on **how AI (Mydo by Biloop) transforms five industries**:

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

The site is plain static HTML, so it publishes with no build step. Two options:

### Option A — GitHub Actions (recommended, already wired up)
1. Push this branch (done by the automation).
2. In the repo, go to **Settings → Pages**.
3. Under **Build and deployment → Source**, choose **GitHub Actions**.
4. The included workflow (`.github/workflows/pages.yml`) deploys automatically on push to `main` or this branch. You can also trigger it manually via **Actions → Deploy to GitHub Pages → Run workflow**.

### Option B — Deploy from a branch
1. **Settings → Pages → Source → Deploy from a branch**.
2. Select the branch and the `/ (root)` folder, then **Save**.

Once live, the site is available at:

```
https://saheerlulu.github.io/mydo/
```

(blogs at `https://saheerlulu.github.io/mydo/blogs/<name>.html`)

## Using the LinkedIn posts

Open [`linkedin-posts/README.md`](linkedin-posts/README.md) for the full posting plan and tips. Before posting, replace each `[link to blog]` placeholder with the live GitHub Pages URL of the matching deep-dive.

---

© 2026 Biloop. Mydo is a product of Biloop. · [biloop.ai](https://biloop.ai) · info@biloop.ai
