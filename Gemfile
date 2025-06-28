source "https://rubygems.org"

# Use github-pages for maximum compatibility
gem "github-pages", group: :jekyll_plugins
gem "webrick", "~> 1.7.0"

# Theme
gem "just-the-docs"

# Required for Ruby 3.4+ compatibility
gem "base64"
gem "bigdecimal"
gem "csv"
gem "logger"
gem "ostruct"

# Additional plugins
group :jekyll_plugins do
  gem "jekyll-remote-theme"
  gem "jekyll-include-cache"
end

# Override specific gems for Ruby 3.2+ compatibility
gem "liquid", "~> 4.0.4"
gem "jekyll", "~> 3.9.5"

# For compatibility with GitHub Pages, pin these
gem "kramdown-parser-gfm", "~> 1.1.0"
gem "kramdown", "~> 2.3.1"
gem "jekyll-feed", "~> 0.12"

# Pin these versions to avoid conflicts
gem "google-protobuf", "< 3.24.0"
gem "sass-embedded", "~> 1.58.0"
gem "nokogiri", "~> 1.12.5"

