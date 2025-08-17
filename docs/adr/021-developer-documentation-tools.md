# ADR-021: Developer Documentation Tools Selection

## Status

Accepted

## Context

The Unipress project needs comprehensive developer documentation to support:
- New developer onboarding
- API reference documentation
- Code examples and tutorials
- Architecture explanations
- Development guidelines

We need to choose appropriate tools for generating and maintaining developer documentation that integrates well with our existing Python ecosystem and development workflow.

## Decision

We will use **Sphinx** with **Myst-Parser** for developer documentation, complemented by **autodoc** for API reference generation.

### Documentation Stack
- **Sphinx**: Primary documentation generator
- **Myst-Parser**: Markdown support for Sphinx
- **autodoc**: Automatic API documentation from docstrings
- **sphinx-rtd-theme**: Read the Docs theme for professional appearance
- **sphinx-autobuild**: Live reload during development

## Alternatives Considered

### 1. Sphinx (Chosen Solution)
**Pros:**
- **Industry Standard**: De facto standard for Python documentation
- **Rich Ecosystem**: Extensive plugins and themes
- **Autodoc Integration**: Automatic API documentation from docstrings
- **Multiple Output Formats**: HTML, PDF, ePub, LaTeX
- **Search Functionality**: Built-in search capabilities
- **Version Control**: Support for multiple versions
- **Read the Docs Integration**: Seamless hosting on readthedocs.org
- **Extensibility**: Highly customizable with extensions

**Cons:**
- **Learning Curve**: Complex configuration for advanced features
- **Setup Overhead**: Initial setup requires more configuration
- **Performance**: Can be slow for large projects

### 2. MkDocs
**Pros:**
- **Simple Setup**: Easy to configure and get started
- **Markdown Native**: Uses Markdown as primary format
- **Fast**: Quick build times
- **Material Theme**: Beautiful, modern theme
- **Git Integration**: Good integration with Git workflows

**Cons:**
- **Limited Python Integration**: No built-in autodoc support
- **Less Extensible**: Fewer plugins compared to Sphinx
- **No API Documentation**: Requires manual API documentation
- **Limited Search**: Basic search functionality

### 3. pdoc
**Pros:**
- **Python Native**: Designed specifically for Python
- **Zero Configuration**: Works out of the box
- **Modern Output**: Clean, modern HTML output
- **Type Hints Support**: Excellent support for type annotations
- **Fast**: Very fast generation

**Cons:**
- **Limited Customization**: Less flexible than Sphinx
- **No Tutorial Support**: Focused on API docs only
- **No Search**: No built-in search functionality
- **Limited Theming**: Few theme options

### 4. Docusaurus
**Pros:**
- **React-based**: Modern, component-based approach
- **Versioning**: Excellent version control support
- **Search**: Advanced search capabilities
- **Internationalization**: Built-in i18n support
- **Plugin Ecosystem**: Rich plugin ecosystem

**Cons:**
- **JavaScript/React**: Requires JavaScript knowledge
- **Overkill**: Too complex for Python project documentation
- **Setup Complexity**: More complex setup than needed
- **Performance**: Slower than Python-native solutions

### 5. Jupyter Book
**Pros:**
- **Interactive**: Support for Jupyter notebooks
- **Modern**: Built on modern web technologies
- **Educational**: Great for tutorials and educational content
- **Publishing**: Easy publishing to various platforms

**Cons:**
- **Not API-focused**: Better for tutorials than API docs
- **Complexity**: Overkill for simple API documentation
- **Dependencies**: Heavy dependencies for simple docs

## Technical Implementation

### Dependencies
```toml
[dependency-groups]
dev = [
    "sphinx>=7.0.0",
    "myst-parser>=2.0.0",
    "sphinx-rtd-theme>=1.3.0",
    "sphinx-autobuild>=2021.3.14",
    "sphinx-copybutton>=0.5.0",
    "sphinx-tabs>=3.4.0",
]
```

### Project Structure
```
docs/
├── conf.py                 # Sphinx configuration
├── index.md               # Main documentation page
├── api/                   # API documentation
│   ├── base_game.md       # BaseGame class docs
│   ├── settings.md        # Settings system docs
│   └── sound.md           # Sound system docs
├── tutorials/             # Tutorials and guides
│   ├── getting_started.md # Getting started guide
│   ├── game_development.md # Game development guide
│   └── deployment.md      # Deployment guide
├── architecture/          # Architecture documentation
│   ├── overview.md        # System overview
│   └── components.md      # Component details
└── _static/              # Static assets (CSS, JS, images)
```

### Sphinx Configuration
```python
# conf.py
project = 'Unipress'
copyright = '2024, jgrynczewski'
author = 'jgrynczewski'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'myst_parser',
    'sphinx_rtd_theme',
    'sphinx_copybutton',
    'sphinx_tabs.tabs',
]

html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'navigation_depth': 4,
    'collapse_navigation': False,
    'sticky_navigation': True,
    'includehidden': True,
    'titles_only': False,
}
```

### Documentation Workflow
1. **Write docstrings** in Python code using Google/NumPy style
2. **Create Markdown files** for tutorials and guides
3. **Generate documentation** with `sphinx-build`
4. **Preview locally** with `sphinx-autobuild`
5. **Deploy** to Read the Docs or GitHub Pages

## Rationale

### Why Sphinx?
- **Python Ecosystem Integration**: Perfect fit for Python projects
- **Autodoc Support**: Automatic API documentation from docstrings
- **Professional Standards**: Industry standard for Python documentation
- **Extensibility**: Can grow with project needs
- **Hosting Options**: Excellent integration with Read the Docs

### Why Myst-Parser?
- **Markdown Support**: Familiar format for most developers
- **Sphinx Compatibility**: Works seamlessly with Sphinx
- **Rich Features**: Supports advanced Markdown features
- **Easy Migration**: Can use existing Markdown files

### Why Read the Docs Theme?
- **Professional Appearance**: Clean, modern design
- **Mobile Responsive**: Works well on all devices
- **Search Functionality**: Built-in search capabilities
- **Version Control**: Support for multiple documentation versions

## Consequences

### Positive
- **Professional Documentation**: Industry-standard documentation
- **Automatic API Docs**: Reduces maintenance burden
- **Search Functionality**: Users can easily find information
- **Version Control**: Support for multiple documentation versions
- **Hosting Integration**: Easy deployment to Read the Docs
- **Extensibility**: Can add features as project grows

### Considerations
- **Learning Curve**: Team needs to learn Sphinx configuration
- **Setup Time**: Initial setup requires more configuration
- **Maintenance**: Need to maintain docstrings and documentation
- **Build Time**: Documentation generation can be slow for large projects

### Implementation Requirements
- Add Sphinx dependencies to pyproject.toml
- Create documentation directory structure
- Configure Sphinx with appropriate extensions
- Write comprehensive docstrings for all public APIs
- Create tutorials and guides
- Set up automated documentation building in CI/CD
- Configure hosting on Read the Docs or GitHub Pages

## Future Considerations
- **Internationalization**: Add support for multiple languages
- **Interactive Examples**: Add Jupyter notebook integration
- **API Testing**: Integrate documentation with API testing
- **Performance Optimization**: Optimize build times for large projects
- **Custom Themes**: Develop custom theme if needed

## Related Decisions
- [ADR-003: Development Tools (ruff, pytest)](003-development-tools-ruff-pytest.md)
- [ADR-006: Type Checking (mypy)](006-type-checking-mypy.md)
- [ADR-020: UML Documentation (PlantUML)](020-uml-documentation-plantuml.md)

## References
- [Sphinx Documentation](https://www.sphinx-doc.org/)
- [Myst-Parser Documentation](https://myst-parser.readthedocs.io/)
- [Read the Docs Theme](https://sphinx-rtd-theme.readthedocs.io/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [NumPy Docstring Guide](https://numpydoc.readthedocs.io/en/latest/format.html)
