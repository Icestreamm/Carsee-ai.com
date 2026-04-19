# Deploying CarSee to Cloudflare (Wrangler)

This site is **static HTML/CSS/JS**. Use **Cloudflare Pages** and the Wrangler CLI command **`wrangler pages deploy`**, not **`wrangler deploy`**.

| Command | Use case |
|--------|----------|
| **`wrangler pages deploy .`** | Upload static files to **Cloudflare Pages** (this project). |
| **`wrangler deploy`** | Deploy a **Cloudflare Worker** only when you have Worker source (e.g. `src/index.ts` + `main` in `wrangler.toml`). This repo does not use that for the marketing site. |

## One-time setup

1. Install dependencies (from this folder):

   ```bash
   npm install
   ```

2. Log in to Cloudflare:

   ```bash
   npx wrangler login
   ```

3. **Project name** — In [wrangler.toml](wrangler.toml), `name = "carsee-website"` is the **Pages project name** Wrangler will create or target. Change it to match an existing Cloudflare Pages project, or keep it and Wrangler will create a new project on first deploy (subject to your account permissions).

## Deploy

From the repository root (where [index.html](index.html) and [wrangler.toml](wrangler.toml) live):

```bash
npm run deploy:pages
```

Equivalent:

```bash
npx wrangler pages deploy .
```

To override the project name for a single run:

```bash
npx wrangler pages deploy . --project-name=your-pages-project-name
```

## Uploaders and TypeScript

If a **no-build uploader** complains about TypeScript: this workspace includes a nested **[my-video/](my-video/)** Remotion/TypeScript app. That folder is **not** excluded automatically by `wrangler pages deploy` (Wrangler skips common paths like `node_modules` and `.git`, but not arbitrary folders). To keep uploads small or avoid shipping that subproject, move `my-video` outside this tree, or deploy from a CI artifact that only contains the static site files.

## References

- [Wrangler `pages deploy`](https://developers.cloudflare.com/workers/wrangler/commands/#deploy-1)
- [Cloudflare Pages](https://developers.cloudflare.com/pages/)
