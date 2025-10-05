from django.shortcuts import render
from django.http import HttpResponse

from .models import Movie

# Create your views here.

def home(request):
    #return HttpResponse("</h1>Welcome to Home Page</h1>")
    #return render(request, 'home.html')
    #return render(request, 'home.html', {'name': 'Sara Osorio'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm': searchTerm, 'movies': movies})


def about(request):
    #return HttpResponse("</h1>Welcome to About Page</h1>")
    return render(request, 'about.html')

def singup(request):
    email = request.POST.get('email')
    return render(request, 'singup.html', {'email': email})


import matplotlib.pyplot as plt 
import matplotlib 
import io 
import urllib, base64 

def generate_plot_base64(labels, counts, title, xlabel, ylabel, fig_size=(10, 6)):
    matplotlib.use('Agg') 
    
    bar_positions = range(len(labels))

    plt.figure(figsize=fig_size) 
    plt.bar(bar_positions, counts, width=0.8, align='center')
    
    plt.title(title) 
    plt.xlabel(xlabel) 
    plt.ylabel(ylabel) 
    plt.xticks(bar_positions, labels, rotation=90)
    plt.subplots_adjust(bottom=0.35)
    
    buffer = io.BytesIO() 
    plt.savefig(buffer, format='png') 
    buffer.seek(0) 
    plt.close() 
    
    graphic = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return graphic

def statistics_view(request): 
    # --- 1. PROCESAMIENTO: AÑOS (Ya lo tenías) ---
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year')
    movie_counts_by_year = {}
    for year in years:
        if year:
            movies_in_year = Movie.objects.filter(year=year)
        else:
            movies_in_year = Movie.objects.filter(year__isnull=True)
            year = "N/A"
        count = movies_in_year.count()
        if count > 0:
            movie_counts_by_year[year] = count
    
    # 2. GENERAR GRÁFICA DE AÑOS
    year_graphic = generate_plot_base64(
        labels=movie_counts_by_year.keys(),
        counts=movie_counts_by_year.values(),
        title='Movies per Year',
        xlabel='Year',
        ylabel='Number of Movies'
    )

    # --- 3. PROCESAMIENTO: GÉNEROS (Lógica de conteo múltiple) ---
    genres_data = Movie.objects.values_list('genre', flat=True)
    genre_counts = {}
    for full_genre_string in genres_data:
        if full_genre_string:
            individual_genres = full_genre_string.split(',')
            for genre in individual_genres:
                clean_genre = genre.strip()
                if clean_genre:
                    genre_counts[clean_genre] = genre_counts.get(clean_genre, 0) + 1
    
    # Ordenar géneros para la gráfica
    sorted_genres = dict(sorted(genre_counts.items(), key=lambda item: item[1], reverse=True))

    # 4. GENERAR GRÁFICA DE GÉNEROS
    genre_graphic = generate_plot_base64(
        labels=sorted_genres.keys(),
        counts=sorted_genres.values(),
        title='Total Movies per Genre',
        xlabel='Genre',
        ylabel='Total Appearances',
        fig_size=(12, 7) # Tamaño más grande para los nombres de género
    )
    
    # 5. RENDERIZAR AMBAS GRÁFICAS
    context = {
        'year_graphic': year_graphic,
        'genre_graphic': genre_graphic
    }
    return render(request, 'statistics.html', context)


