import re
import os
from mkdocs.plugins import BasePlugin
from urllib.parse import urlsplit
from pathlib import Path

class PageListPlugin(BasePlugin):
    """
    A MkDocs plugin to generate dynamic lists of pages based on `{pagelist}` commands in markdown files.
    It supports grouping by folder, filtering by tags, and limiting the number of links.
    """

    def __init__(self):
        self.page_list_info = []

    def on_nav(self, nav, config, files):
        self.nav = nav
        self.files = files

        for file in files:
            self._gather_page_list_info(file)

    def _gather_page_list_info(self, file):
        try:
            with open(file.abs_src_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            try:
                with open(file.abs_src_path, 'r', encoding='latin-1') as f:
                    content = f.read()
            except Exception as e:
                print(f"Error reading file {file.abs_src_path}: {e}")
                return

        for match in re.finditer(r'\{pagelist(?:\s+(\d+|g$|i$)\s*(.*?))?(?:\|\s*(.*))?\}', content):
            page_list_code = match.group(0)
            page_url = file.url
            self.page_list_info.append({'page_url': page_url, 'page_list_code': page_list_code})

    def on_post_page(self, output, page, config):
        matches = re.finditer(r'\{pagelist(?:\s+(\d+|g$|i$)\s*(.*?))?(?:\|\s*(.*))?\}', output) # Nothing is generated if either digit, 'i' or 'g' is not the first argument

        for match in matches:
            if match.group(1) == 'i':
                page_list_output = self.generate_page_list_info_output(self.page_list_info, page)
                output = output.replace(match.group(0), page_list_output, 1)
            else:
                group_folders = match.group(1) == 'g'
                tags_to_filter = match.group(2).strip().split() if match.group(2) else page.meta.get('tags', [])
                limit = int(match.group(1)) if match.group(1) and match.group(1).isdigit() else None
                if limit == 0:  # We expect limit of generated links to be defined all the time (if 'g' or 'i' option is not used). 0 means unlimited.
                    limit = None
                folders_to_filter = match.group(3).strip().split() if match.group(3) else []

                filtered_list = self._format_links_by_folder_and_tag(tags_to_filter, page, config, group_folders, limit, folders_to_filter)
                output = output.replace(match.group(0), filtered_list, 1)

        return output

    def generate_page_list_info_output(self, page_list_info, current_page):
        output = '<ol class="page-list-info">'
        for info in page_list_info:
            relative_path = self._get_relative_path(current_page.url, info['page_url'])
            output += f"<li><a href='{relative_path}'>{info['page_url']}</a> - {info['page_list_code']}</li>"
        output += '</ol>'
        return output

    def _format_links_by_folder_and_tag(self, tags_to_filter, current_page, config, group_folders, limit, folders_to_filter):
        folder_groups = {}

        # Normalize the folders_to_filter list
        normalized_folders_to_filter = [folder.lower() for folder in folders_to_filter]

        for file in self.files:
            if file.page is not None and self._page_has_tags(file.page, tags_to_filter):
                folder_name = self._extract_folder_name(file.page.url).lower()

                # Check if the folder name matches any of the specified folders to filter
                if folders_to_filter and folder_name not in normalized_folders_to_filter:
                    continue  # Skip this page if its folder is not in the folders_to_filter list

                if folder_name not in folder_groups:
                    folder_groups[folder_name] = []
                folder_groups[folder_name].append(file.page)

        result = '<div class="pagelist">'
        item_count = 0  # Initialize item count

        for folder, pages in folder_groups.items():
            if group_folders:
                result += f'<h3 class="pagelistheading">{folder.capitalize()}</h3>\n'
            result += '<ul class="pagelistlist">\n'
            for page in pages:
                if limit is not None and item_count >= limit:
                    break  # Stop adding links once the limit is reached
                relative_path = self._get_relative_path(current_page.url, page.url)
                if current_page.url != page.url:  # Don't generate link for myself
                    result += f'<li><a href="{relative_path}">{page.title}</a></li>\n'
                    item_count += 1
            result += '</ul>\n'
            if limit is not None and item_count >= limit:
                break  # Break the outer loop as well if the limit is reached

        result += '</div>'

        return result

    def _page_has_tags(self, page, tags_to_filter):
        if not tags_to_filter:
            return False  # Return False if no tags to filter

        page_tags = set(page.meta.get('tags', []))
        any_tags = {tag for tag in tags_to_filter if not tag.startswith('+') and not tag.startswith('-')}
        all_tags = {tag.lstrip('+') for tag in tags_to_filter if tag.startswith('+')}
        exclude_tags = {tag.lstrip('-') for tag in tags_to_filter if tag.startswith('-')}

        any_match = any(tag in page_tags for tag in any_tags) if any_tags else True
        all_match = all(tag in page_tags for tag in all_tags)
        exclude_match = not any(tag in page_tags for tag in exclude_tags)

        return any_match and all_match and exclude_match

    def _extract_folder_name(self, url):
        path_parts = Path(urlsplit(url).path).parts
        relevant_parts = path_parts[:-1]
        folder_title = ' '.join(part.capitalize() for part in relevant_parts)
        return folder_title

    def _get_relative_path(self, from_url, to_url):
        from_parts = Path(urlsplit(from_url).path).parts
        to_parts = Path(urlsplit(to_url).path).parts
        common_prefix_length = len(os.path.commonprefix([from_parts, to_parts]))
        relative_path = ['..'] * (len(from_parts) - common_prefix_length - 1) + list(to_parts[common_prefix_length:])
        return '/'.join(relative_path)

    def on_files(self, files, config):
        self.files = files
        return files
