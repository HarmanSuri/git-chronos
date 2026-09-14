# git-chronos
> **A lightweight CLI to visualize messy git logs as easy-to-read timelines in your terminal**

---

## 🧐 The Problem

Many developers love how easy and quick the git CLI is for managing commits, but as projects grow, it can be hard to visualize commit trees and see who's done what. git-chronos is a simple wrapper for git which displays git log's output in an easy-to-read timeline, rather than large blocks of text.

---

## ✨ Key Features

- **Visual Commit Timeline:** Renders Git history as a clean, colour-coded ASCII timeline.
- **Contributor Stats:** Displays author contribution ratios with visual progress bars.
- **Filtering Options:** Filter output by author (`--author`) or total commit count (`-n`).
- **Terminal-Friendly:** Automatic colour support with fallback for CI/CD environments (`-- no-colour`).
- **Smart Error Guard:** Gracefully handles non-Git directories and empty repository states.

---
