# PageListPlugin for MkDocs

PageListPlugin is a plugin for MkDocs that dynamically generates lists of pages based on tags, folders, and other criteria directly within your markdown files. It's especially useful for creating dynamic references to other parts of your documentation based on shared tags or directory structure. It may need tweaking for your needs.  The use of grouping by folders is helpful if you use the Diátaxis framework to organise your documents.  I have all my documents listed under the folders - Tutorials, How-to, Reference, 
Explanation. Tags are used to cross connect across those folders with features, functions or intended audience. 


## Installation

To install the plugin, use the following command:

```bash
pip install mkdocs-pagelist-plugin
```

For Github Actions add the following line in the appropriate place in the `ci.yml` file:

```yaml
- run: pip install mkdocs-pagelist-plugin  
```


## Usage

To use the PageListPlugin, add it to your `mkdocs.yml` configuration file under the plugins section:

```yaml
plugins:
  - search
  - pagelist
```

> **Note**: If you have no `plugins` entry in your config file yet, you'll need to add it before adding PageListPlugin, as MkDocs enables only the `search` plugin by default.



## Examples

> **Note**: You always have to specify either 'i', 'g', or digit as a first argument. Setting `0` as a first argument means unlimited amount of generated links.

- **List other pages sharing the same tags as the current page**:
  ```
  {pagelist}
  ```

- **List 10 pages sharing the same tags as the current page**:
  ```
  {pagelist 10}
  ```

- **Group pages by folder, sharing the same tags as the current page**:
  ```
  {pagelist g}
  ```

- **List 5 pages tagged with 'draft'**:
  ```
  {pagelist 5 draft}
  ```

- **List all pages tagged with 'draft'**:
  ```
  {pagelist 0 draft}
  ```

- **List 10 pages tagged with either 'draft' or 'leads'**:
  ```
  {pagelist 10 draft leads}
  ```

- **List all pages with 'leads' tag but exclude those with 'draft' tag**:
  ```
  {pagelist 0 -draft leads}
  ```

- **List all pages tagged with both 'leads' and 'draft' tags but exclude those with 'test' tag**:
  ```
  {pagelist 0 +draft +leads -test}
  ```

- **Group pages by folder, tagged with 'leads'**:
  ```
  {pagelist g leads}
  ```

- **Group pages by folder, tagged with 'leads' but not 'draft'**:
  ```
  {pagelist g leads -draft}
  ```

- **List pages tagged with 'leads' in the 'how-to' folder**:
  ```
  {pagelist 10 leads | how-to}
  ```

- **Generate a report of all `{pagelist}` commands used across the site**:
  ```
  {pagelist i}
  ```

## HTML and CSS

The rendered code looks something like this:

```html
<div class="pagelist">
	<h3 class="pagelistheading">{folder.capitalize()}</h3>
	<ul class="pagelistlist">
		<li><a href="../../{page.url}">{page.title}</a></li>
	</ul>
</div>
```

## License

This project is licensed under the MIT License.

---
