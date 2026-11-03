# Yanbin (Tracy) Xu — academic website

Source for https://Tracy2033.github.io/. The custom domain remains on its existing host until a separately approved cutover.

## Update content

Edit papers.json for papers, summaries, status and links; profile.json for biography and affiliation; teaching.json for courses; service.json for committee roles and presentations. The homepage links directly to Yanbin_Xu_CV.pdf; replace that file to update the CV. There is no separate CV navigation tab.

All source files and assets are kept at repository root for straightforward browser uploads. build.py assembles five pages and puts assets under dist/assets and PDFs under dist/files. Layout is in base.html and build.py; styles are in style.css. No third-party build dependencies are required.

```sh
python3 build.py
python3 check.py
python3 -m http.server 8765 --directory dist
```

The GitHub Pages workflow is manual. After editing files, run Actions → Build and deploy academic website → Run workflow. It builds, checks links and publishes dist. No DNS records are changed by this workflow.

legacy-assets.json retains former custom-domain download paths for a future domain migration. Publication statuses should only be changed when verified. AI work is labelled research in development.
