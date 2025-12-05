# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh
- [@vitejs/plugin-react-swc](https://swc.rs/) for Fast Refresh

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.

---

## 🚀 GitHub Pages Deployment

This project uses **Vite** and the **`gh-pages`** package for deployment to GitHub Pages. The deployment target is the **`gh-pages`** branch, which contains only the optimized build files.

### Setup and Configuration

1. **Install the deployment tool:**

    ```bash
    npm install gh-pages --save-dev
    ```

2. **Configure `package.json`:**
    - Set the `homepage` URL.
    - Add `predeploy` (to run the build) and `deploy` scripts.

    ```json
    "homepage": "[https://mavhawk64.github.io/valorant-collections](https://mavhawk64.github.io/valorant-collections)",
    "scripts": {
      // ... existing scripts
      "predeploy": "npm run build",
      "deploy": "gh-pages -d dist"
    },
    ```

3. **Configure `vite.config.js`:**
    - Set the `base` path to your repository name to ensure assets load correctly.

    ```javascript
    // vite.config.js
    export default defineConfig({
      // ... plugins
      base: "/valorant-collections/"
    })
    ```

### Deployment Workflow

After making and committing changes to your primary development branch (`main`), run the following command to build the production assets and update the live site:

```bash
npm run deploy
