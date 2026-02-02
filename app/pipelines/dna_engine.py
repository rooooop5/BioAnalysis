from app.bio.basic_dna_services import analyze_dna, dna_validity, rev_complement, transcription, complement, translation
from app.schemas.dna_schemas import DNAPipelineContext, DNAPipelineSteps, InvocationSource


def validation_step(ctx: DNAPipelineContext):
    dna = str(ctx.dna)
    result = dna_validity(dna)
    if not result['is_valid']:
        ctx.stop_pipeline = True
        ctx.error = result['detail']
    return result


def complement_step(ctx: DNAPipelineContext):
    return complement(ctx.dna)


def reverse_complement_step(ctx: DNAPipelineContext):
    return rev_complement(ctx.dna)


def transcription_step(ctx: DNAPipelineContext):
    return transcription(ctx.dna, ctx.strand_type)


def translation_step(ctx: DNAPipelineContext):
    return translation(ctx.dna)


def analyzation_step(ctx: DNAPipelineContext):
    return analyze_dna(ctx.dna)


mapping = {
    DNAPipelineSteps.validate: validation_step,
    DNAPipelineSteps.reverse_complement: reverse_complement_step,
    DNAPipelineSteps.complement: complement_step,
    DNAPipelineSteps.transcribe: transcription_step,
    DNAPipelineSteps.translate: translation_step,
    DNAPipelineSteps.analyze: analyzation_step,
}


def pipeline_handler(step_result, step):
    pipeline_result = {}
    pipeline_result[step] = step_result
    return pipeline_result


def dna_engine(ctx: DNAPipelineContext, steps_list):
    ctx.result = {}
    if DNAPipelineSteps.validate not in steps_list:
        steps_list.insert(0, DNAPipelineSteps.validate)
        ctx.result['message'] = 'Auto added validation step'
    for step in steps_list:
        biofunction = mapping[step]
        step_result = biofunction(ctx)
        if ctx.invocation_source == InvocationSource.pipeline:
            (ctx.result).update(pipeline_handler(step_result=step_result, step=step))
            if ctx.stop_pipeline:
                stop_message = {
                    'message': 'Pipeline stopped',
                    'error_message': ctx.error,
                    'Pipeline stopped at step': step,
                }
                ctx.result['PIPELINE STOPPED'] = stop_message
                break
        if ctx.invocation_source == InvocationSource.endpoint:
            ctx.result = step_result
