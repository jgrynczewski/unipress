# ADR-023: Documentation Hosting Platform Selection

## Status

**Accepted** - 2025-08-18

## Context

The Unipress project has comprehensive Sphinx-based developer documentation that needs to be hosted online for easy access by developers, contributors, and users. We need to choose between different hosting platforms that can automatically build and serve our documentation.

## Decision

We will use **Read the Docs** as our primary documentation hosting platform, with GitHub Pages as a backup option.

## Rationale

### Platform Comparison

| Feature | Read the Docs | GitHub Pages | Netlify | Vercel |
|---------|---------------|--------------|---------|--------|
| **Sphinx Support** | ✅ Native | ⚠️ Manual setup | ⚠️ Manual setup | ⚠️ Manual setup |
| **Auto-build** | ✅ Automatic | ✅ GitHub Actions | ✅ Git hooks | ✅ Git hooks |
| **Version Control** | ✅ Multiple versions | ⚠️ Manual | ⚠️ Manual | ⚠️ Manual |
| **Search** | ✅ Built-in | ❌ No | ❌ No | ❌ No |
| **Analytics** | ✅ Built-in | ❌ No | ✅ Yes | ✅ Yes |
| **Custom Domain** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Cost** | ✅ Free | ✅ Free | ✅ Free tier | ✅ Free tier |
| **Integration** | ✅ GitHub | ✅ GitHub | ✅ GitHub | ✅ GitHub |

### Why Read the Docs?

1. **Native Sphinx Support**: Read the Docs is specifically designed for Sphinx documentation
2. **Automatic Versioning**: Automatically builds documentation for different Git branches and tags
3. **Built-in Search**: Provides full-text search across all documentation
4. **Professional Appearance**: Clean, professional design that's familiar to developers
5. **Zero Configuration**: Minimal setup required for Sphinx projects
6. **Community Standard**: Widely used in the Python ecosystem

### GitHub Pages as Backup

GitHub Pages will be configured as a backup option using GitHub Actions for:
- Manual deployment when needed
- Custom builds for specific branches
- Alternative hosting if Read the Docs is unavailable

## Consequences

### Positive

- **Professional Documentation**: Read the Docs provides a professional, searchable documentation site
- **Automatic Updates**: Documentation automatically updates with each commit
- **Version Control**: Multiple versions of documentation available (latest, stable, specific releases)
- **SEO Benefits**: Better discoverability through search engines
- **Community Integration**: Familiar platform for Python developers

### Negative

- **External Dependency**: Relies on third-party service availability
- **Limited Customization**: Some design constraints compared to self-hosted solutions
- **Build Time**: Documentation builds may take a few minutes after commits

### Neutral

- **Setup Complexity**: Initial setup requires configuration but is straightforward
- **Maintenance**: Minimal ongoing maintenance required

## Implementation

### Read the Docs Setup

1. **Account Creation**
   ```bash
   # Sign up at https://readthedocs.org
   # Connect GitHub account
   # Import unipress repository
   ```

2. **Configuration File**
   Create `.readthedocs.yml` in project root:
   ```yaml
   version: 2
   
   build:
     os: ubuntu-22.04
     tools:
       python: "3.12"
   
   python:
     install:
       - method: pip
         path: .
         extra_requirements:
           - dev
   
   sphinx:
     configuration: docs/sphinx/conf.py
     fail_on_warning: false
   
   formats:
     - pdf
     - epub
   
   # Build documentation in docs/sphinx/ directory
   # Output directory: docs/sphinx/_build/html
   ```

3. **Documentation Structure**
   ```
   docs/
   ├── sphinx/
   │   ├── conf.py          # Sphinx configuration
   │   ├── index.md         # Main documentation page
   │   ├── api/             # API documentation
   │   ├── tutorials/       # Tutorials and guides
   │   ├── architecture/    # Architecture documentation
   │   └── _static/         # Static assets
   └── README.md            # Documentation overview
   ```

### GitHub Pages Backup Setup

1. **GitHub Actions Workflow**
   Create `.github/workflows/docs.yml`:
   ```yaml
   name: Build and Deploy Documentation
   
   on:
     push:
       branches: [ master ]
       paths: [ 'docs/**', 'unipress/**', 'pyproject.toml' ]
     pull_request:
       branches: [ master ]
   
   jobs:
     build-docs:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         
         - name: Set up Python
           uses: actions/setup-python@v4
           with:
             python-version: '3.12'
         
         - name: Install uv
           uses: astral-sh/setup-uv@v2
           with:
             version: "latest"
         
         - name: Install dependencies
           run: |
             uv sync --group dev
         
         - name: Build documentation
           run: |
             cd docs/sphinx
             uv run sphinx-build -b html . _build/html
         
         - name: Deploy to GitHub Pages
           if: github.ref == 'refs/heads/master'
           uses: peaceiris/actions-gh-pages@v3
           with:
             github_token: ${{ secrets.GITHUB_TOKEN }}
             publish_dir: ./docs/sphinx/_build/html
   ```

2. **GitHub Pages Settings**
   - Enable GitHub Pages in repository settings
   - Set source to "GitHub Actions"
   - Configure custom domain if needed

### Documentation URLs

- **Primary**: `https://unipress.readthedocs.io/`
- **Backup**: `https://jgrynczewski.github.io/unipress/`
- **Development**: `https://unipress.readthedocs.io/en/latest/`

### Configuration Updates

1. **Update Sphinx Configuration**
   ```python
   # docs/sphinx/conf.py
   
   # Read the Docs specific settings
   on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
   
   if on_rtd:
       html_theme = 'sphinx_rtd_theme'
   else:
       html_theme = 'sphinx_rtd_theme'
   
   # Add Read the Docs analytics
   html_extra_path = ['_static']
   ```

2. **Update README.md**
   Add documentation links:
   ```markdown
   ## Documentation
   
   - **Developer Documentation**: [Read the Docs](https://unipress.readthedocs.io/)
   - **API Reference**: [API Docs](https://unipress.readthedocs.io/en/latest/api/)
   - **Architecture**: [Architecture Docs](https://unipress.readthedocs.io/en/latest/architecture/)
   ```

## Alternatives Considered

### GitHub Pages Only
- **Pros**: Simple, integrated with GitHub
- **Cons**: No built-in search, manual versioning, less professional appearance
- **Decision**: Rejected - lacks professional features needed for developer documentation

### Self-hosted Solution
- **Pros**: Full control, custom features
- **Cons**: High maintenance, hosting costs, security concerns
- **Decision**: Rejected - overkill for project needs, high maintenance burden

### Netlify/Vercel
- **Pros**: Modern features, good performance
- **Cons**: No native Sphinx support, requires custom build setup
- **Decision**: Rejected - better suited for web applications than documentation

## References

- [Read the Docs Documentation](https://docs.readthedocs.io/)
- [Sphinx Documentation](https://www.sphinx-doc.org/)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
