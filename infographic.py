import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import textwrap


def get_infographic(account_longevity, total_watch_time, watch_hours_per_week, top_series_title, top_series,
                    top_series_by_episodes, top_movie, top_movie_title, first_show_info):
    im = Image.open('img/template-new.png')
    sns.set_context('poster', font_scale=1, rc={"grid.linewidth": 0})
    # plt.axes([0.0, 0.0, 1.5, 3.3])
    plt.axes([0.0, 0.0, 1, 2])
    plt.axis('off')
    font_type = {
        'medium': 'fonts/Montserrat-Medium.ttf',
        'bold': 'fonts/Montserrat-Bold.ttf'
    }
    highlight_font = ImageFont.truetype(font_type['bold'], 45)
    regular_font = ImageFont.truetype(font_type['medium'], 32)

    draw = ImageDraw.Draw(im)

    # Account age
    account_longevity_x = 345
    draw.text((account_longevity_x, 240), 'Desde', font=regular_font, fill='white')
    draw.text((account_longevity_x + 125, 230), account_longevity.start, font=highlight_font, fill='white')
    draw.text((account_longevity_x + 5, 315), 'Hasta', font=regular_font, fill='white')
    draw.text((account_longevity_x + 125, 305), f'{account_longevity.years} años {account_longevity.months} meses',
              font=highlight_font, fill='white')

    # Watching time
    watching_time_x = 350
    draw.text((watching_time_x, 400), f'{int(total_watch_time[0]):,}', font=highlight_font, fill='white')
    draw.text((watching_time_x + 125, 410), 'horas totales viendo contenido', font=regular_font, fill='white')
    draw.text((watching_time_x, 470), f'{watch_hours_per_week:.1f}', font=highlight_font, fill='white')
    draw.text((watching_time_x + 125, 480), 'horas por semana', font=regular_font, fill='white')

    # Top Series
    top_series_title = textwrap.shorten(top_series_title, width=30)
    top_series_x = 65
    draw.text((top_series_x, 695), 'Serie más vista', font=regular_font, fill='white')
    draw.text((top_series_x, 735), top_series_title, font=highlight_font, fill='white')
    draw.text((top_series_x, 800), f'{top_series.duration_hours.values[0]:.0f} Horas', font=regular_font, fill='white')
    draw.text((top_series_x + 220, 800), f'{top_series_by_episodes.plays.values[0]} episodios', font=regular_font,
              fill='white')

    # Top Movie
    top_movie_x = 230
    top_movie_title = textwrap.shorten(top_movie_title, width=35)
    draw.text((top_movie_x, 980), 'Película más vista', font=regular_font, fill='white')
    draw.text((top_movie_x, 1020), top_movie_title, font=highlight_font, fill='white')
    draw.text((top_movie_x, 1075), f'{top_movie.head(1).plays.values[0]} reproducciones', font=regular_font,
              fill='white')

    # First content
    first_show_x = 230
    firs_show_title = textwrap.shorten(first_show_info[0], width=35)
    draw.text((first_show_x, 1220), firs_show_title, font=highlight_font, fill='white')
    draw.text((first_show_x, 1275), 'Primer contenido visto', font=regular_font, fill='white')

    return im
