from app.models import FarmlandDataset, TaskInfo, PlotInfo, SurveyRecord, SampleRecord, AnalysisResult


def _create_dataset_from_completed_plot(db, task_id, plot_id):
    """地块完成时自动创建数据集记录"""
    task = db.query(TaskInfo).filter(TaskInfo.ID == task_id, TaskInfo.SFSC == 0).first()
    if not task:
        return
    plot = db.query(PlotInfo).filter(PlotInfo.ID == plot_id, PlotInfo.SFSC == 0).first()
    if not plot:
        return

    existing = db.query(FarmlandDataset).filter(
        FarmlandDataset.RWID == task_id,
        FarmlandDataset.DKID == plot_id,
        FarmlandDataset.SFSC == 0
    ).first()
    if existing:
        return

    survey = db.query(SurveyRecord).filter(
        SurveyRecord.RWID == task_id, SurveyRecord.DKID == plot_id, SurveyRecord.SFSC == 0
    ).first()

    sample = db.query(SampleRecord).filter(
        SampleRecord.RWID == task_id, SampleRecord.DKID == plot_id, SampleRecord.SFSC == 0
    ).first()

    analysis = db.query(AnalysisResult).filter(
        AnalysisResult.RWID == task_id, AnalysisResult.DKID == plot_id, AnalysisResult.SFSC == 0
    ).first()

    dataset = FarmlandDataset(
        RWID=task_id,
        DKID=plot_id,
        RWMC=task.RWMC,
        TBH=plot.TBH,
        JD=plot.JD,
        WD=plot.WD,
        CYRQ=sample.CYRQ if sample and sample.CYRQ else None,
        DXBW=survey.DXBW if survey else None,
        YXTCHD=survey.YXTCHD if survey else None,
        GCZD=None,
        RZ=analysis.RZ if analysis else None,
        ZDGX=survey.ZDGX if survey else None,
        SWDYX=None,
        NTLW=None,
        ZAYS=None,
        GGNL=None,
        PSNL=survey.PSNL if survey else None,
        PHZ=analysis.PHZ if analysis else None,
        YJZ=analysis.YJZ if analysis else None,
        YXL=analysis.YXP if analysis else None,
        SXJ=analysis.XJK if analysis else None,
        SRXYLZL=analysis.SRXYLZL if analysis else None,
        DLMC=None,
        JQCD=None,
        BZ=None,
        GD=analysis.GE if analysis else None,
        ZG=analysis.ZG if analysis else None,
        ZS=analysis.ZS if analysis else None,
        Q=analysis.QIAN if analysis else None,
        G=analysis.GE_CHROME if analysis else None,
        GDZLDJ=None,
        ZLFJ=None,
    )
    db.add(dataset)
