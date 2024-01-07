<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class PreviewController extends Controller
{
    public function showPreview(Request $request)
    {
        $url = $request->input('url');

        if ($url) {
            if (!filter_var($url, FILTER_VALIDATE_URL)) {
                die('Not a valid URL');
            }
            if (strtolower(parse_url($url, PHP_URL_SCHEME)) === 'file') {
                die('File scheme is not allowed');
            }

            $html = file_get_contents($url, false, stream_context_create(['http' => [
                'method' => $request->input('method', 'GET'),
                'ignore_errors' => true,
                'follow_location' => false,
            ]]));

            preg_match('/<title[^>]*>(.+)<\/title>/i', $html, $matches_title);
            preg_match('/<meta\s+name="description"\s+content="([^"]+)/i', $html, $matches_desc);

            $status_code = null;
            $http_response_header = $http_response_header ?? [];
            if (isset($http_response_header[0])) {
                preg_match('/HTTP\/\d\.\d\s+(\d+)/', $http_response_header[0], $status_code);
                $status_code = $status_code[1] ?? null;
            }

            $request->session()->put('url', $url);

            return view('preview', [
                'url' => $url,
                'title' => $matches_title[1] ?? $url,
                'description' => $matches_desc[1] ?? null,
                'statusCode' => $status_code,
                'responseHeader' => $status_code !== '200' ? implode("\n", $http_response_header) : null,
            ]);
        }

        return view('preview');
    }
}
