<!DOCTYPE html>
<html>

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Preview Card</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.3/css/bulma.min.css">
</head>

<body>
    <section class="section">
        <div class="container">
            <div class="column is-10 is-offset-1">
                <a href="/">⬅ HOME</a>
                <form action="{{ route('preview.show') }}" method="GET">
                    <input class="input" type="text" name="url" value="{{ request('url') }}" placeholder="https://example.com">
                </form>
                <br>
                @if (isset($url))
                    <div class="column is-6 is-offset-3">
                        <h3 class="title is-5">Preview card</h3>
                        <div class="box">
                            <h3 class="title">{{ $title }}</h3>
                            @if ($description)
                                <p>{{ $description }}</p>
                            @endif
                            <a href="{{ $url }}">{{ $url }}</a>
                        </div>
                    </div>

                    @if ($statusCode !== '200')
                        <div class="column is-6 is-offset-3">
                            <h3 class="title is-5">Debug</h3>
                            <pre>{{ $responseHeader }}</pre>
                        </div>
                    @endif
                @endif
            </div>
        </div>
    </section>
</body>

</html>
