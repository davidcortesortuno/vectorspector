import matplotlib


# -----------------------------------------------------------------------------


def plot_vector_field(self,
                      x_min, x_max,
                      y_min, y_max,
                      v_component='vz',
                      normalize_data=True,
                      nx=100, ny=100,
                      interpolator='scipy',
                      xlim=None,
                      ylim=None,
                      figsize=(8., 8.),
                      cmap='gist_earth',
                      hsv_map=False,
                      cmap_alpha=1.,
                      quiver_map=None,
                      colorbar=False,
                      colorbar_label='',
                      quiver_type='raw_cmap',
                      quiver_color='k',
                      pivot='middle',
                      nx_q=20,
                      ny_q=20,
                      frame=True,
                      predefined_axis=None,
                      x_label=r'$x$',
                      y_label=r'$y$',
                      savefig=None,
                      interpolator_method=None,
                      interpolator_hsv_method=None,
                      interpolator_quiver_method=None,
                      **quiver_args
                      ):

        """
        Make a 2D plot from the data extracted of the VTK file, using
        a colormap with interpolated values.
        IT IS NECESSARY to run the extract_data() function before.
        If a new range of z_values is required, simply reassign the self.z_min
        and self.z_max attributes
        When setting quiver_type as interpolated, the numbers of arrows can be
        controled specifying the nx_q and ny_q parameeters, which are the
        number of entities along x and y respectively.
        OPTIONS:
        x_min, x_max        :: Range of spatial x values to be used in the 2D
                               plot to interpolate the data for the colormap
        y_min, y_max        :: Range of spatial y values to be used in the 2D
                               plot to interpolate the data for the colormap
        v_component         :: Component of the vector field that is going
                               to be shown as the magnitude of every entity
                               in a colormap. By default, it is plotted
                               the z component magnitude of the vectors.
                               Options:
                                    'vx', 'vy', 'vz'
        normalize_data      :: Set False if the colorbar ticks values are in the
                               range of the real data. By default, the colormap is
                               normalised from -1 to 1
        nx, ny              :: Resolution in the x and y directions
                               for the interpolations using the data points,
                               i.e. the number of divisions
                               between x_min and x_max; y_min and y_max
        interpolator        :: The interpolation from the irregular mesh
                               of the VTK file is done by default using
                               'scipy'. It is also possible
                               to use matplotlib.mlab.griddata passing
                               the option 'natgrid'
                               If an error about not having griddata from
                               matplotlib, is raised, it can be installed
                               from the instructions in the print statement
        xlim, ylim          :: Plot ranges in the x and y directions, given
                               as a list with the [min, max] values
        figsize             :: Dimensions of the plot as a tuple,
                               (8, 8) by default
        cmap                :: Palette of the colourmap (not considered if
                               using the hsv_map option)
        hsv_map             :: With this option the colormap is going to use
                               the HSV palette, where the x and y
                               components of the
                               vectors are mapped into the Hue values and the z
                               component is done in the S and V, so that the
                               maximum z values are shown in white and the
                               minimum in black. For 2 dimensional vector
                               fields, this makes the colormap to be only black
                               (since all the z components are set to zero),
                               thus this option can be passed as:
                                    '2d' or '3d'.
                               The 2d option set S and V as 1, so the plot
                               shows the full color. The 3d option makes the
                               mapping black or white according to the z
                               component of the field.
                               This mapping is useful for showing a vector
                               field without a quiver plot.
        cmap_alpha          :: Transparency value of the colourmap
        quiver_map          :: Colour palette of the arrows of the vector
                               field. By default it is the inverted
                               palette of cmap
        colorbar            :: Set True to plot a color bar with the palette
        colorbar_label      :: String with the colorbbar label
                               (shown rotated in 270 degrees)
        quiver_type         :: By default the quiver plot is not interpolated,
                               it shows all the data points in the specified
                               spatial ranges (raw data), and it is shown with
                               a colormap.  This option lets the user choose to
                               interpolate the vector field and if a colormap
                               or a single color is used. The options are:
                                    'interpolated_cmap', 'interpolated_color',
                                    'raw_cmap', 'raw_color'
        quiver_color        :: Arrow color if one of the 'color' options was
                               specified in the quiver_type argument
        pivot               :: By default we make the arrows to be drawn at the
                               center of the grid nodes. This option is from
                               the matplotlib quiver function
        nx_q, ny_q          :: Resolution in the x and y directions for the
                               arrows in the quiver plot if one of the
                               interpolated quiver_type options are passed
                               (number of divisions between x_min and x_max;
                               y_min and y_max). By default: 20 x 20 arrows are
                               drawn
        frame               :: Frame of the plot
        predefined_axis     :: Can be a predefined matplotlib axis object to
                               show the plot on it. This is useful to make
                               a grid of plots
        x_label, y_label    :: Axes labels
        savefig             :: String with the route and/or name of the
                               file if it is going to
                               be saved. The format is obtained from the name,
                               e.g. 'my_plot.pdf'
        interpolator_method   :: Method for scipy or natgrid, default: 'cubic'
                                 or 'nn'
        interpolator_hsv_method     :: Method for scipy, for the HSV mapping.
                                       Default: 'linear'
        interpolator_quiver_method :: Method for scipy or natgrid when
                                      interpolating the quiver plot, default:
                                      'linear' or 'nn'
        **quiver_args       :: Any extra keyword arguments for the quiver plot
        TODO:
            Add polar components
            Add titles
        """

        # Set the interpolator methods according to the arguments
        if not interpolator_method:
            if interpolator == 'scipy':
                interpolator_method = 'cubic'
            elif interpolator == 'natgrid':
                interpolator_method = 'nn'
            else:
                print('Specify a valid interpolation method')
                return

        # The HSV interpolation is better with linear (cubic messes up things)
        if hsv_map:
            if not interpolator_hsv_method:
                interpolator_hsv_method = 'linear'

        if (quiver_type == 'interpolated_cmap'
                or quiver_type == 'interpolated_color'):
            if not interpolator_quiver_method:
                if interpolator == 'scipy':
                    interpolator_quiver_method = 'linear'
                elif interpolator == 'natgrid':
                    interpolator_quiver_method = 'nn'

        # Save the array with the filtered data indexes
        # (we put it here, since if the z ranges are updated, this will update
        # the values)
        self.data_filter = (self.z_max > self.z) & (self.z > self.z_min)
        if len(np.where(self.data_filter == True)[0]) == 0:
            print('No data in specified range!')
            return

        # Dictionary to use a specific vector component
        comp = {'vx': 0, 'vy': 1, 'vz': 2}

        # Leave only the components between the specified range of z values
        x = self.x[self.data_filter]
        y = self.y[self.data_filter]
        z = self.z[self.data_filter]

        # Define the side of the grid as the radius plus an extra
        # space to properly center the system in the plot
        # rgrid = x_max + 10

        xi = np.linspace(x_min, x_max, nx)
        yi = np.linspace(y_min, y_max, ny)

        # If the HSV map option was passed, make the mapping according
        # to the vector field components
        if hsv_map:
            # Angles of every spin (which defines the colour
            # when varying the H value in HSV)
            angles = np.arctan2(self.vf[:, comp['vy']][self.data_filter],
                                self.vf[:, comp['vx']][self.data_filter])

            # Redefine angles < 0 to got from pi to 2 pi
            angles[angles < 0] = angles[angles < 0] + 2 * np.pi

            # The m_z values will be white for m_z = +1 and
            # black for m_z = -1
            alphas = np.copy(self.vf[:, comp['vz']][self.data_filter])
            alphas_inv = np.copy(self.vf[:, comp['vz']][self.data_filter])

            if hsv_map == '3d':
                alphas[alphas > 0] = 1
                alphas[alphas < 0] = alphas[alphas < 0] + 1

                alphas_inv[alphas_inv > 0] = 1 - alphas_inv[alphas_inv > 0]
                alphas_inv[alphas_inv < 0] = 1

                # hsv_array = np.array((angles, np.ones_like(angles), alphas)).T
                hsv_array = np.array((angles, alphas_inv, alphas)).T

            elif hsv_map == '2d':
                hsv_array = np.array((angles,
                                      np.ones_like(angles),
                                      np.ones_like(angles)
                                      )
                                     ).T
            else:
                print('Specify a dimension for the HSV mapping')
                return

            def convert_to_rgb(a):
                return np.array(colorsys.hsv_to_rgb(a[0] / (2 * np.pi),
                                                    a[1],
                                                    a[2]
                                                    )
                                )

            hsv_array = np.array(list(map(convert_to_rgb, hsv_array)))

        # Extract the z_component of the vector field
        # (or m_component if specified) to do the colormap
        if not hsv_map:
            try:
                if interpolator == 'natgrid':
                    # ml.griddata may need the natgrid complement if matplotlib was
                    # installed with pip. You can get it doing
                    # git clone https://github.com/matplotlib/natgrid.git
                    # and then: sudo pip install .
                    # from the git folder

                    zi = matplotlib.mlab.griddata(x, y,
                                                  self.vf[:, comp[v_component]][
                                                      self.data_filter],
                                                  xi, yi,
                                                  interp=interpolator_method)

                elif interpolator == 'scipy':
                    # Use scipy interpolation
                    # We need to generate tuples
                    # Ideas from:
                    # http://stackoverflow.com/questions/9656489/
                    # griddata-scipy-interpolation-not-working-giving-nan

                    xi, yi = np.meshgrid(xi, yi)

                    # The method can be changed, but the 'nearest' is not
                    # working well with the values outside the simulation mesh
                    zi = scipy.interpolate.griddata((x, y),
                                                    self.vf[:, comp[v_component]][
                                                        self.data_filter],
                                                    (xi, yi),
                                                    method=interpolator_method
                                                    )

                # Mask the NaN values (generally they are outside the
                # mesh defined in the simulation) so they are not plotted
                zi = np.ma.masked_where(np.isnan(zi), zi)

            except Exception('Interpolation Error'):
                print('An error ocurred while interpolating the data. '
                      'One of the possible reasosn is that '
                      'matplotlib.mlab.griddata may need the natgrid '
                      'complement in case matplotlib was '
                      'installed with pip. You can get natgrid by doing \n'
                      'git clone https://github.com/matplotlib/natgrid.git \n'
                      'and then: \n sudo pip install . \n'
                      'from the git folder'
                      )
                return

        # Otherwise, use the HSV colour map for the vector field
        else:
            xi, yi = np.meshgrid(xi, yi)
            zi = scipy.interpolate.griddata((x, y),
                                            hsv_array,
                                            (xi, yi),
                                            method=interpolator_hsv_method,
                                            fill_value=1
                                            )

        # Quiver data in a dictionary
        quiv = {}

        # Interpolate the arrows for the quiver plot if arrow_resolution was
        # passed as True
        # This option ONLY works with mlab natgrid (CHECK!) --> Try scipy
        if (quiver_type == 'interpolated_cmap'
                or quiver_type == 'interpolated_colour'):

            (quiv['vx'],
             quiv['vy'],
             quiv['vz'],
             xi_q, yi_q) = self.interpolate_field(x, y,
                                                  x_min, x_max,
                                                  y_min, y_max,
                                                  nx_q=nx_q, ny_q=ny_q,
                                                  interpolator=interpolator,
                                                  interpolator_method=interpolator_quiver_method
                                                  )

        # ---------------------------------------------------------------------
        # Now plot in matplotlib ----------------------------------------------
        # ---------------------------------------------------------------------
        # Use a predefined axis if possible
        if predefined_axis:
            ax = predefined_axis
        else:
            fig = plt.figure(figsize=figsize, frameon=frame)
            ax = fig.add_subplot(111)

        if not hsv_map:
            # Plot the colour map with the interpolated values of v_i
            ax.pcolormesh(xi, yi, zi, cmap=plt.get_cmap(cmap), vmin=-1, vmax=1,
                          alpha=cmap_alpha)
        else:
            # Plot the colour map with the HSV colours
            ax.imshow(zi, interpolation='None',
                      extent=[np.min(xi), np.max(xi),
                              np.min(yi), np.max(yi)],
                      vmin=-1, vmax=1,
                      origin='lower'
                      )
        if colorbar:
            if hsv_map:
                cmap_cb = matplotlib.cm.get_cmap(name='hsv')
            else:
                cmap_cb = matplotlib.cm.get_cmap(name=cmap)

            if normalize_data or hsv_map:
                norm = matplotlib.colors.Normalize(-1, 1)
            else:
                norm = matplotlib.colors.Normalize(vmin=np.min(zi),
                                                   vmax=np.max(zi))

            # Add axes for the colorbar with respect to the top image
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="3%", pad=0.05)

            # Colorbar
            cbar = matplotlib.colorbar.ColorbarBase(cax,
                                                    cmap=cmap_cb,
                                                    norm=norm,
                                                    # ticks=[-1, 0, 1],
                                                    orientation='vertical',
                                                    )

            cbar.set_label(colorbar_label, rotation=270)

            # Label HSV colorbar accordingly
            if hsv_map:
                cbar.set_ticks([1, 0, -1])
                cbar.set_ticklabels([r'$2\pi$', r'$\pi$', r'$0$'])
                # cbar.update_ticks()

        if not quiver_map:
            quiver_map = cmap + '_r'

        # Use whole data if the vector field is not inerpolated
        if (quiver_type == 'raw_cmap'
                or quiver_type == 'raw_colour'):
            quiv['vx'] = self.vf[:, 0][self.data_filter],
            quiv['vy'] = self.vf[:, 1][self.data_filter]
            quiv['vz'] = self.vf[:, 2][self.data_filter]

            xi_q, yi_q = x, y

        if (quiver_type == 'interpolated_cmap'
                or quiver_type == 'raw_cmap'):
            ax.quiver(xi_q,
                      yi_q,
                      quiv['vx'],
                      quiv['vy'],
                      # paint the vectors according to the
                      # component of m_component
                      quiv[v_component],
                      cmap=quiver_map,
                      pivot=pivot,
                      **quiver_args
                      )
        elif (quiver_type == 'interpolated_colour'
                or quiver_type == 'raw_colour'):
            ax.quiver(xi_q,
                      yi_q,
                      quiv['vx'],
                      quiv['vy'],
                      color=quiver_color,
                      pivot=pivot,
                      **quiver_args
                      )
        elif not quiver_type:
            pass
        else:
            print('Specify an option for the quiver plot')
            return

        if not frame:
            ax.axis('off')

        if xlim:
            ax.set_xlim(xlim)
        if ylim:
            ax.set_ylim(ylim)

        # Axes labels
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)

        if savefig:
            plt.savefig(savefig, bbox_inches='tight')

# plt.show()