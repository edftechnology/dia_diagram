def analysis_pre_defined_design(self):
    """
    Análise de uma configuração existente do Conjunto da Câmara de Empuxo
    (Thrust Chamber Assembly (TCA)).

    Função temporária para testar a análise 'pura' do Conjunto da Câmara de
    Empuxo (Thrust Chamber Assembly (TCA)).

    A ideia é, uma vez satisfatória, migrar esta função (ou renomear)
    para o 'design' em si, que não terá mais etapas
    relacionado ao design.

    :param self: Obrigatório.
        Instância da classe.

    :return None.
    """

    logger.debug("Entering TCA analysis for pre-defined design...")

    self.geometry.fill_params()

    self.performance.fill_params()

    self.cooling.thermal_analysis(self.geometry, self.performance,
                                    self.feasibility, self.output)

    self.structure.cooling_jacket_structural_analysis(
        self.cooling, self.output)
    
    if self.cooling.settings.is_there_radiative_nozzle_cooling:
        self.structure.radiative_nozzle_preliminary_structural_analysis(
            self.performance, self.geometry, self.cooling)

    logger.info("TCA analysis complete.")

    logger.info("Exp. I_sp (vac) = %.1f s,",
                self.performance.isp_vac_exp / g_0)

    if self.cooling.settings.is_there_radiative_nozzle_cooling:
        max_temp_jack = max(self.cooling.gas_side_wall_temperature[
            :(self.cooling.grid.jacket_index + 1)])
        max_temp_rad = max(self.cooling.gas_side_wall_temperature[
            (self.cooling.grid.jacket_index + 1):])
        logger.info("Maximum wall temperature (jacket section) = %.1F K",
                    max_temp_jack)
        logger.info("Maximum wall temperature (rad. section) = %.1F K",
                    max_temp_rad)
    else:
        logger.info("Maximum wall temperature = %.1F K",
                    max(self.cooling.gas_side_wall_temperature))

    logger.info("Maximum coolant temperature = %.1F K",
                max(self.cooling.jacket.liq_temperature))

    delta_t = self.cooling.jacket.liq_temperature[0] - \
        self.cooling.jacket.liq_temperature[-1]

    logger.info("Total increase in coolant temperature = %.1F K", delta_t)
