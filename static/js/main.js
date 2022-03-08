
    jQuery(document).ready(function () {
      jQuery('.tooltip').tooltipster({
        theme: 'tooltipster-borderless',
        arrow: false,
        delay: 80,
        distance: 1,
        contentAsHTML: true,
        trackOrigin: true
      });

      jQuery('#south-east').on("mouseover", function () { jQuery('#ser').css("display", "block"); });
      jQuery('#south-east').on("mouseleave", function () { jQuery('#ser').css("display", "none"); });

      jQuery('#mid-central').on("mouseover", function () { jQuery('#mcr').css("display", "block"); });
      jQuery('#mid-central').on("mouseleave", function () { jQuery('#mcr').css("display", "none"); });

      jQuery('#south-central').on("mouseover", function () { jQuery('#scr').css("display", "block"); });
      jQuery('#south-central').on("mouseleave", function () { jQuery('#scr').css("display", "none"); });

      jQuery('#south-west').on("mouseover", function () { jQuery('#swr').css("display", "block"); });
      jQuery('#south-west').on("mouseleave", function () { jQuery('#swr').css("display", "none"); });

      jQuery('#north-east').on("mouseover", function () { jQuery('#ner').css("display", "block"); });
      jQuery('#north-east').on("mouseleave", function () { jQuery('#ner').css("display", "none"); });

      jQuery('#mid-atlantic').on("mouseover", function () { jQuery('#mar').css("display", "block"); });
      jQuery('#mid-atlantic').on("mouseleave", function () { jQuery('#mar').css("display", "none"); });

      jQuery('#north-central').on("mouseover", function () { jQuery('#ncr').css("display", "block"); });
      jQuery('#north-central').on("mouseleave", function () { jQuery('#ncr').css("display", "none"); });

      jQuery('#pacific-north').on("mouseover", function () { jQuery('#pnr').css("display", "block"); });
      jQuery('#pacific-north').on("mouseleave", function () { jQuery('#pnr').css("display", "none"); });

      jQuery('#pacific-south').on("mouseover", function () { jQuery('#psr').css("display", "block"); });
      jQuery('#pacific-south').on("mouseleave", function () { jQuery('#psr').css("display", "none"); });

      jQuery('#nca-nevada').on("mouseover", function () { jQuery('#ncnr').css("display", "block"); });
      jQuery('#nca-nevada').on("mouseleave", function () { jQuery('#ncnr').css("display", "none"); });

    });
